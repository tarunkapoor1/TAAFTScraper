from flask import Flask, request, jsonify, render_template_string
import os
from scrape_ai_tools import scrape_ai_tools

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Tools Scraper</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
        }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input, button { padding: 8px; }
        button { 
            background-color: #4CAF50; 
            color: white; 
            border: none; 
            cursor: pointer; 
        }
        button:hover { background-color: #45a049; }
        .result { 
            margin-top: 20px; 
            padding: 15px; 
            border: 1px solid #ddd; 
        }
    </style>
</head>
<body>
    <h1>AI Tools Scraper</h1>
    <form method="POST">
        <div class="form-group">
            <label for="num_tools">Number of tools to scrape (1-1000):</label>
            <input type="number" id="num_tools" name="num_tools" min="1" max="1000" required>
        </div>
        <div class="form-group">
            <label for="task">Task/category filter (optional):</label>
            <input type="text" id="task" name="task">
        </div>
        <button type="submit">Start Scraping</button>
    </form>
    {% if result %}
    <div class="result">
        <h2>Scraping Result:</h2>
        <p>{{ result }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            num_tools = int(request.form.get('num_tools', 10))
            task = request.form.get('task', '').strip()
            
            # Get the API key from environment variable
            api_key = os.getenv('SCRAPER_API_KEY')
            if not api_key:
                return render_template_string(HTML_TEMPLATE, 
                    result="Error: SCRAPER_API_KEY environment variable not set")

            # Run the scraper with user inputs
            result = scrape_ai_tools(api_key, num_tools, task)
            return render_template_string(HTML_TEMPLATE, 
                result=f"Successfully scraped {len(result)} tools. Check ai_tools.csv for results.")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, 
                result=f"Error: {str(e)}")
    
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
