from localLLM import LocalLLM

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
                
# Define the host and port
host = '0.0.0.0'
port = 8000

class CustomHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        query = query_components.get('query', [None])[0]

        # Get model from headers
        model = self.headers.get('model', 1)

        global my_llm  # Access the global llm instance
        my_llm.select_model(model)

        if query is None:
            # Respond with an error message if query is missing
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = '{"error": "Missing query parameter"}'
        else:
            # Respond to GET requests with the query information
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            llm_response = my_llm.generate_response(query)
            response = f'{{"model": {model}, "response": "{llm_response}"}}'

        self.wfile.write(response.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=CustomHandler):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on {host}:{port}')

    httpd.serve_forever()


if __name__ == '__main__':
    my_llm = LocalLLM()  # Create the llm instance here
    run(handler_class=lambda *args, **kwargs: CustomHandler(*args, **kwargs))
