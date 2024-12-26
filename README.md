# AI Tools Scraper

A Python script that scrapes AI tool information and converts it to CSV format.

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

3. Create a .env file with your API key:
```bash
SCRAPER_API_KEY=your_api_key_here
```

4. Run the script:
```bash
python scrape_ai_tools.py
```

The script will prompt you for:
- Number of AI tools to scrape (1-1000)
- Task/category to filter by (optional, press Enter to scrape all tasks)

## Output

The script generates an `ai_tools.csv` file containing the following information for each AI tool:
- Name
- Task/Category
- Rating
- Number of saves
- Pricing
- URL

## Deployment on Digital Ocean

1. Create a new Droplet on Digital Ocean
2. SSH into your Droplet:
```bash
ssh root@your_droplet_ip
```

3. Install required packages:
```bash
apt update
apt install python3-pip python3-venv git
```

4. Clone and setup:
```bash
git clone [repository-url]
cd ai-tools-scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
echo "SCRAPER_API_KEY=your_api_key_here" > .env
```

6. Run the script:
```bash
python scrape_ai_tools.py
```

## License

MIT License
