# Vercel Serverless Function Entry Point
# This file handles incoming requests and forwards them to the Flask app

from app import app

# Vercel Serverless Function handler
def handler(request):
    """
    Vercel Serverless Function handler
    Converts Vercel request format to WSGI format
    """
    # Get the WSGI environment from the request
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string,
        'SERVER_NAME': request.headers.get('host', 'localhost'),
        'SERVER_PORT': '443',
        'HTTP_HOST': request.headers.get('host', 'localhost'),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': request.body,
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    for key, value in request.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Collect response
    response_data = []
    
    def start_response(status, headers):
        response_data.append((status, headers))
    
    # Call the Flask app
    result = app(environ, start_response)
    
    # Build response
    if response_data:
        status, headers = response_data[0]
        body = b''.join(result)
        
        return {
            'statusCode': int(status.split()[0]),
            'headers': dict(headers),
            'body': body.decode('utf-8'),
        }
    
    return {
        'statusCode': 500,
        'body': 'Internal Server Error',
    }

# Export for Vercel
app_handler = handler