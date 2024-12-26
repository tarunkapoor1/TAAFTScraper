from flask import Flask, request, jsonify
import os
from scrape_ai_tools import scrape_ai_tools

app = Flask(__name__)

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400

        num_tools = int(data.get('num_tools', 10))
        task = data.get('task', '').strip()

        if not 1 <= num_tools <= 1000:
            return jsonify({
                'status': 'error',
                'message': 'num_tools must be between 1 and 1000'
            }), 400
        
        # Use environment variable if set, otherwise use default API key
        api_key = os.getenv('SCRAPER_API_KEY', '8QR2EG5JQ7W6BSU8IQJDHRUW8UU2JL97ABZH4TUEWRSKCK74AJN9NGQFOAMJA9MD4N3Z45OLHB6USX4J')

        # Run the scraper with user inputs
        result = scrape_ai_tools(api_key, num_tools, task)
        
        # Return JSON response
        return jsonify({
            'status': 'success',
            'count': len(result),
            'tools': result
        })
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'AI Tools Scraper API',
        'endpoints': {
            '/api/scrape': {
                'method': 'POST',
                'description': 'Scrape AI tools data',
                'parameters': {
                    'num_tools': 'Number of tools to scrape (1-1000)',
                    'task': 'Optional task/category filter'
                },
                'example': {
                    'request': {
                        'num_tools': 10,
                        'task': 'writing'
                    }
                }
            }
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
