# AI Tools Scraper

A Python application that scrapes AI tool information and converts it to CSV format. Available both as a command-line tool and a web interface.

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd ai-tools-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set your API key:
   - The application comes with a default API key
   - To use your own key, create a .env file:
   ```bash
   SCRAPER_API_KEY=your_api_key_here
   ```

4. Run the application:

### Command Line Usage
```bash
python scrape_ai_tools.py
```
The script will prompt you for:
- Number of AI tools to scrape (1-1000)
- Task/category to filter by (optional, press Enter to scrape all tasks)

### Web Interface Usage
```bash
python app.py
```
Then visit http://localhost:8080 in your browser to access the web interface.

## Output

The script generates an `ai_tools.csv` file containing the following information for each AI tool:
- Name
- Task/Category
- Rating
- Number of saves
- Pricing
- URL

## Deployment on Digital Ocean

1. Create a new App on Digital Ocean App Platform:
   - Go to Digital Ocean Dashboard
   - Click "Create" -> "Apps"
   - Choose your GitHub repository

2. Configure the app:
   - (Optional) Set Environment Variables:
     - SCRAPER_API_KEY=your_api_key_here (if you want to use your own key)
   - Build Command: `pip install -r requirements.txt`
   - Run Command: Will be automatically detected from Procfile

3. Deploy the app:
   - Click "Deploy"
   - Wait for the build and deployment to complete
   - Access your app at the provided URL

## Development

The application consists of two main components:
- `scrape_ai_tools.py`: Core scraping functionality
- `app.py`: Web interface using Flask

The Procfile specifies the web process type for Digital Ocean deployment using gunicorn.

## License

MIT License
