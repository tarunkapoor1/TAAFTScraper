# AI Tools Scraper API

A REST API that scrapes AI tool information from theresanaiforthat.com, providing structured data about AI tools including name, task, rating, saves, pricing, and URL.

## API Documentation

### Base URL
```
https://your-app-url/
```

### Endpoints

#### 1. GET /
Returns API information and available endpoints.

Response:
```json
{
  "status": "success",
  "message": "AI Tools Scraper API",
  "endpoints": {
    "/api/scrape": {
      "method": "POST",
      "description": "Scrape AI tools data",
      "parameters": {
        "num_tools": "Number of tools to scrape (1-1000)",
        "task": "Optional task/category filter"
      }
    }
  }
}]
```

#### 2. POST /api/scrape
Scrapes AI tool information based on provided parameters.

Request Body:
```json
{
  "num_tools": 10,
  "task": "writing"
}
```

Response:
```json
{
  "status": "success",
  "count": 10,
  "tools": [
    {
      "name": "Tool Name",
      "task": "Tool Category",
      "rating": 4.5,
      "saves": 38,
      "pricing": "Free",
      "url": "https://tool-url.com"
    }
  ]
}
```

### Error Responses

```json
{
  "status": "error",
  "message": "Error description"
}
```

Common error messages:
- "No JSON data provided"
- "num_tools must be between 1 and 1000"
- "Invalid input: [details]"
- "Server error: [details]"

## Deployment

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
   - Access your API at the provided URL

## Development

The application consists of two main components:
- `scrape_ai_tools.py`: Core scraping functionality
- `app.py`: REST API implementation using Flask

The Procfile specifies the web process type for Digital Ocean deployment using gunicorn.

## License

MIT License
