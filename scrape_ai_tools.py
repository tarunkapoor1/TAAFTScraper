import requests
from bs4 import BeautifulSoup
import time
import random
import os

def make_request(url, params, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Making request attempt {attempt + 1}/{max_retries}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                raise
    return None

def get_user_input():
    while True:
        try:
            num_tools = int(input("How many AI tools would you like to scrape? (1-1000): "))
            if 1 <= num_tools <= 1000:
                break
            print("Please enter a number between 1 and 1000.")
        except ValueError:
            print("Please enter a valid number.")
    
    task = input("Enter the task/category to filter by (press Enter for all tasks): ").strip()
    return num_tools, task

def scrape_ai_tools(api_key, num_tools_wanted=10, task_filter=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    base_url = 'https://theresanaiforthat.com/'
    ai_tools = []

    try:
        page = 1

        while len(ai_tools) < num_tools_wanted:
            url = f"{base_url}?page={page}"
            if task_filter:
                # Convert task to URL-friendly format and add to query
                task_slug = task_filter.lower().replace(' ', '-')
                url = f"{base_url}{task_slug}/?page={page}"
            
            print(f"\nFetching page {page} from {url}")

            # ScrapingBee API configuration
            scrapingbee_url = "https://app.scrapingbee.com/api/v1/"
            params = {
                'api_key': api_key,
                'url': url,
                'render_js': 'true',
                'wait': '5000',
                'premium_proxy': 'true',
                'block_resources': 'false'
            }

            response = make_request(scrapingbee_url, params, headers)
            if not response:
                print("Failed to get response after all retries")
                break
            
            print(f"Response status code: {response.status_code}")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all tool items
            tools = soup.find_all('li', class_='li')
            print(f"Total tools found: {len(tools)}")

            if not tools:
                print(f"No more tools found on page {page}")
                break

            for tool in tools:
                if len(ai_tools) >= num_tools_wanted:
                    break

                try:
                    # Extract all required fields
                    name_element = tool.find('a', class_='ai_link')
                    name = name_element.text.strip() if name_element else None

                    task_element = tool.find('a', class_='task_label')
                    task = task_element.text.strip() if task_element else None

                    rating_element = tool.find('div', class_='average_rating')
                    rating = float(rating_element.text.strip()) if rating_element else None

                    saves_element = tool.find('div', class_='saves')
                    saves = int(saves_element.text.strip()) if saves_element else None

                    pricing_element = tool.find('a', class_='ai_launch_date')
                    pricing = pricing_element.text.strip() if pricing_element else None

                    url_element = tool.find('a', class_='external_ai_link')
                    url = url_element['href'] if url_element and 'href' in url_element.attrs else None

                    # Skip if any required field is missing
                    if not all([name, task, rating, saves, pricing, url]):
                        continue

                    # Skip if task filter is set and doesn't match
                    if task_filter and task_filter.lower() not in task.lower():
                        continue

                    # Clean up URL
                    if url and not url.startswith('http'):
                        url = base_url.rstrip('/') + url

                    tool_data = {
                        'name': name,
                        'task': task,
                        'rating': rating,
                        'saves': saves,
                        'pricing': pricing,
                        'url': url
                    }
                    
                    print(f"\nExtracted tool data:")
                    print(tool_data)
                    ai_tools.append(tool_data)
                    print(f"Scraped tool {len(ai_tools)}/{num_tools_wanted}: {tool_data['name']}")
                    
                except Exception as e:
                    print(f"Error processing tool: {str(e)}")
                    continue

            # Add a random delay between pages
            delay = random.uniform(2, 5)
            print(f"Waiting {delay:.2f} seconds before next page...")
            time.sleep(delay)
            page += 1

    except Exception as e:
        print(f"An error occurred: {e}")

    return ai_tools

if __name__ == "__main__":
    # Use environment variable if set, otherwise use default API key
    api_key = os.getenv('SCRAPER_API_KEY', '8QR2EG5JQ7W6BSU8IQJDHRUW8UU2JL97ABZH4TUEWRSKCK74AJN9NGQFOAMJA9MD4N3Z45OLHB6USX4J')
    
    num_tools, task = get_user_input()
    result = scrape_ai_tools(api_key, num_tools, task)
    print(f"Successfully scraped {len(result)} tools")
