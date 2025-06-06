"""
Development server for TIL-Tailor.
Serves the static site and rebuilds it when changes are detected.
"""
from http.server import SimpleHTTPRequestHandler, HTTPServer
import subprocess
import os
import shutil


class Handler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler to serve files from output directory."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="output", **kwargs)


def ensure_favicon():
    """Ensure favicon.ico exists in the output directory."""
    static_favicon = os.path.join("static", "as_favicon.ico")
    output_favicon = os.path.join("output", "as_favicon.ico")

    if os.path.exists(static_favicon):
        # Copy favicon to the output directory
        shutil.copy2(static_favicon, output_favicon)
        print("Favicon copied to output directory")
    else:
        print("Warning: as_favicon.ico not found in static directory")


def run_server():
    """Run the development server."""
    subprocess.run(["python", "generator.py"], check=True)
    ensure_favicon()
    server_address = ("", 8080)
    with HTTPServer(server_address, Handler) as httpd:
        print("Serving at http://localhost:8080")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
