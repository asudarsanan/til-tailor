"""
Development server for TIL-Tailor.
Serves the static site and rebuilds it when changes are detected.
"""
from http.server import SimpleHTTPRequestHandler, HTTPServer
import subprocess


class Handler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler to serve files from output directory."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="output", **kwargs)


def run_server():
    """Run the development server."""
    subprocess.run(["python", "generator.py"], check=True)
    server_address = ("", 8080)
    with HTTPServer(server_address, Handler) as httpd:
        print("Serving at http://localhost:8080")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
