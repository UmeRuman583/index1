"""
Web Interface for Google Instant Indexer
Access via browser for easy URL submission
"""

from flask import Flask, render_template, request, jsonify, send_file
from google_indexer import GoogleInstantIndexer
import json
import os
from datetime import datetime
import threading

app = Flask(__name__)

# Global indexer instance
indexer = None
indexing_in_progress = False
last_results = []

def init_indexer(use_api=False, service_account_file=None):
    global indexer
    if use_api and service_account_file and os.path.exists(service_account_file):
        indexer = GoogleInstantIndexer(service_account_file=service_account_file)
    else:
        indexer = GoogleInstantIndexer()

# Initialize on startup
init_indexer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    global indexer
    
    if request.method == 'POST':
        data = request.json
        use_api = data.get('use_google_api', False)
        service_account = data.get('service_account_file', '')
        
        init_indexer(use_api, service_account)
        
        return jsonify({
            'status': 'success',
            'message': 'Configuration updated',
            'api_enabled': indexer.indexing_service is not None
        })
    
    return jsonify({
        'api_enabled': indexer.indexing_service is not None
    })

@app.route('/api/index', methods=['POST'])
def index_urls():
    global indexing_in_progress, last_results
    
    if indexing_in_progress:
        return jsonify({
            'status': 'error',
            'message': 'Indexing already in progress'
        }), 400
    
    data = request.json
    urls = data.get('urls', [])
    
    if not urls:
        return jsonify({
            'status': 'error',
            'message': 'No URLs provided'
        }), 400
    
    # Parse URLs from text (handle newlines)
    if isinstance(urls, str):
        urls = [u.strip() for u in urls.split('\n') if u.strip()]
    
    # Start indexing in background
    def index_task():
        global indexing_in_progress, last_results
        indexing_in_progress = True
        
        try:
            results = indexer.rapid_index_bulk(urls, max_workers=10)
            last_results = results
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.json"
            indexer.save_results(results, filename)
            
        except Exception as e:
            last_results = [{'error': str(e)}]
        finally:
            indexing_in_progress = False
    
    thread = threading.Thread(target=index_task)
    thread.start()
    
    return jsonify({
        'status': 'success',
        'message': f'Started indexing {len(urls)} URLs',
        'url_count': len(urls)
    })

@app.route('/api/status')
def status():
    global indexing_in_progress, last_results
    
    if indexing_in_progress:
        return jsonify({
            'status': 'indexing',
            'in_progress': True
        })
    
    if last_results:
        successful = sum(1 for r in last_results 
                        if r.get('status') == 'success' or 
                        any(m.get('status') == 'success' 
                            for m in r.get('methods_used', [])))
        
        return jsonify({
            'status': 'complete',
            'in_progress': False,
            'total': len(last_results),
            'successful': successful,
            'failed': len(last_results) - successful,
            'results': last_results
        })
    
    return jsonify({
        'status': 'idle',
        'in_progress': False
    })

@app.route('/api/check/<path:url>')
def check_indexing(url):
    result = indexer.check_indexing_status(url)
    return jsonify(result)

if __name__ == '__main__':
    print("=" * 70)
    print("Google Instant Indexer - Web Interface")
    print("=" * 70)
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
