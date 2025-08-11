from flask import Flask, request, Response
import subprocess
import os
import signal
import threading
import time
import requests

app = Flask(__name__)

# Global variable to store Django process
django_process = None

def start_django():
    """Start Django development server"""
    global django_process
    try:
        # Change to the project directory
        os.chdir('/home/ubuntu/salon_agenda')
        
        # Start Django server
        django_process = subprocess.Popen([
            '/home/ubuntu/salao_sys/venv/bin/python',
            'manage.py',
            'runserver',
            '127.0.0.1:8001'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for Django to start
        time.sleep(3)
        
    except Exception as e:
        print(f"Error starting Django: {e}")

def stop_django():
    """Stop Django development server"""
    global django_process
    if django_process:
        django_process.terminate()
        django_process.wait()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_to_django(path):
    """Proxy all requests to Django server"""
    try:
        # Construct the Django URL
        django_url = f"http://127.0.0.1:8001/{path}"
        
        # Forward the request to Django
        if request.method == 'GET':
            resp = requests.get(django_url, params=request.args, headers=request.headers)
        elif request.method == 'POST':
            resp = requests.post(django_url, data=request.get_data(), headers=request.headers)
        elif request.method == 'PUT':
            resp = requests.put(django_url, data=request.get_data(), headers=request.headers)
        elif request.method == 'DELETE':
            resp = requests.delete(django_url, headers=request.headers)
        else:
            resp = requests.request(request.method, django_url, data=request.get_data(), headers=request.headers)
        
        # Create Flask response
        response = Response(
            response=resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
        
        return response
        
    except Exception as e:
        return f"Error proxying request: {e}", 500

if __name__ == '__main__':
    # Start Django in a separate thread
    django_thread = threading.Thread(target=start_django)
    django_thread.daemon = True
    django_thread.start()
    
    try:
        # Start Flask app
        app.run(host='0.0.0.0', port=8000, debug=False)
    finally:
        # Clean up Django process
        stop_django()

