from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import subprocess

PORT = 8000
OUTPUT_DIR = "output"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_DIR, **kwargs)

def run_server():
    # Rebuild the site first
    subprocess.run(["python3", "generator.py"])
    
    # Start server
    server_address = ("", PORT)
    with HTTPServer(server_address, Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()