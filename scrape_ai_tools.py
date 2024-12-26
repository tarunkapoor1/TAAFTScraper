import requests
from bs4 import BeautifulSoup
import csv
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

def scrape_ai_tools(api_key):
    # Get user preferences
    num_tools_wanted, task_filter = get_user_input()
    
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
            
            # Try multiple selectors for tool cards
            tools = []
            selectors = [
                ('div', 'ai_tool_card'),
                ('div', 'tool-card'),
                ('div', 'desk_row'),
                ('a', 'ai_link_wrap')
            ]
            
            for tag, class_name in selectors:
                found_tools = soup.find_all(tag, class_=class_name)
                if found_tools:
                    print(f"Found {len(found_tools)} tools with {tag}.{class_name}")
                    tools = found_tools
                    break
            
            if not tools:
                print("No tools found with standard selectors, trying alternative approach...")
                tools = soup.find_all('div', class_=lambda x: x and ('tool' in x.lower() or 'ai' in x.lower()))
            
            print(f"Total tools found: {len(tools)}")

            if not tools:
                print(f"No more tools found on page {page}")
                break

            for tool in tools:
                if len(ai_tools) >= num_tools_wanted:
                    break

                try:
                    # Extract name
                    name_element = (
                        tool.find('h2') or
                        tool.find('div', class_='title') or
                        tool.find('h3') or
                        tool.find('a', class_='tool-link') or
                        tool.find('div', class_=lambda x: x and 'title' in x.lower())
                    )
                    name = name_element.text.strip() if name_element else ''

                    # Extract description
                    desc_element = (
                        tool.find('div', class_='description') or
                        tool.find('p') or
                        tool.find('div', class_=lambda x: x and 'desc' in x.lower())
                    )
                    description = desc_element.text.strip() if desc_element else ''

                    # Extract category
                    category_element = (
                        tool.find('div', class_='category') or
                        tool.find('span', class_='category') or
                        tool.find('div', class_='task_label_wrap') or
                        tool.find('div', class_=lambda x: x and 'category' in x.lower())
                    )
                    category = category_element.text.strip() if category_element else ''

                    # Skip if task filter is set and doesn't match
                    if task_filter and task_filter.lower() not in category.lower():
                        continue

                    # Extract link
                    link_element = tool.find('a')
                    link = link_element['href'] if link_element and 'href' in link_element.attrs else ''
                    if link and not link.startswith('http'):
                        link = base_url.rstrip('/') + link

                    # Extract image URL
                    img_element = tool.find('img')
                    image_url = img_element['src'] if img_element and 'src' in img_element.attrs else ''
                    if image_url and not image_url.startswith('http'):
                        image_url = 'https:' + image_url if image_url.startswith('//') else base_url.rstrip('/') + image_url

                    # Only add tools that have at least a name
                    if name:
                        tool_data = {
                            'name': name,
                            'description': description,
                            'category': category,
                            'link': link,
                            'image_url': image_url,
                            'page_number': page
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

        # Save to CSV with error handling
        csv_path = 'ai_tools.csv'
        try:
            # First check if we have write permission
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as test_file:
                pass
            
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['name', 'description', 'category', 'link', 'image_url', 'page_number']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for tool in ai_tools:
                    writer.writerow(tool)

            print(f"\nSuccessfully scraped {len(ai_tools)} tools and saved to {csv_path}")
            if task_filter:
                print(f"Filtered by task: {task_filter}")
            
        except PermissionError:
            print(f"Permission denied when trying to write to {csv_path}")
            print("Trying alternative location...")
            
            # Try writing to the user's home directory
            alternative_path = os.path.join(os.path.expanduser('~'), 'ai_tools.csv')
            with open(alternative_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['name', 'description', 'category', 'link', 'image_url', 'page_number']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for tool in ai_tools:
                    writer.writerow(tool)
            print(f"Successfully saved data to alternative location: {alternative_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_key = '8QR2EG5JQ7W6BSU8IQJDHRUW8UU2JL97ABZH4TUEWRSKCK74AJN9NGQFOAMJA9MD4N3Z45OLHB6USX4J'
    scrape_ai_tools(api_key)
