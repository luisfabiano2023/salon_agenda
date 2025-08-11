import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from flask import Flask

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_agenda.settings')

# Setup Django
django.setup()

# Get Django WSGI application
django_app = get_wsgi_application()

# Create Flask app as a wrapper
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Catch all routes and forward to Django"""
    from werkzeug.serving import WSGIRequestHandler
    from werkzeug.wrappers import Request, Response
    
    # Create a WSGI environ from Flask request
    environ = {}
    for key, value in request.environ.items():
        environ[key] = value
    
    # Call Django WSGI app
    response_data = []
    def start_response(status, headers):
        response_data.extend([status, headers])
    
    result = django_app(environ, start_response)
    
    # Convert Django response to Flask response
    response = Response(
        response=b''.join(result),
        status=response_data[0],
        headers=response_data[1]
    )
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

