#!/usr/bin/env python3
"""
Simple HTTP server for serving static files with live reload capability.
Perfect for development of static websites.
"""

import http.server
import os
import socketserver
import sys
import threading
import time
import webbrowser
from pathlib import Path


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files from the landing-page-static directory"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="landing-page-static", **kwargs)

    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Disable caching for development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Custom logging format
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def find_free_port(start_port=8000):
    """Find a free port starting from start_port"""
    port = start_port
    while port < start_port + 100:  # Try 100 ports
        try:
            with socketserver.TCPServer(("", port), None) as test_server:
                return port
        except OSError:
            port += 1
    raise RuntimeError("Could not find a free port")

def open_browser(url, delay=1.5):
    """Open browser after a short delay"""
    time.sleep(delay)
    webbrowser.open(url)

def main():
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Check if the landing-page-static directory exists
    if not os.path.exists("landing-page-static"):
        print("Error: landing-page-static directory not found!")
        print("Make sure you're running this script from the correct directory.")
        sys.exit(1)

    # Find a free port
    try:
        port = find_free_port(8000)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create the server
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("🚀 Static File Server Started!")
            print("=" * 60)
            print(f"📁 Serving files from: {os.path.abspath('landing-page-static')}")
            print(f"🌐 Local URL: http://localhost:{port}")
            print(f"🔗 Network URL: http://127.0.0.1:{port}")
            print("=" * 60)
            print("📝 Tips:")
            print("  • Edit your HTML/CSS files and refresh the browser to see changes")
            print("  • Press Ctrl+C to stop the server")
            print("  • The server disables caching for easier development")
            print("=" * 60)
            print()

            # Open browser in a separate thread
            url = f"http://localhost:{port}"
            browser_thread = threading.Thread(target=open_browser, args=(url,))
            browser_thread.daemon = True
            browser_thread.start()

            print(f"🌍 Opening {url} in your default browser...")
            print(f"📊 Server logs:")
            print()

            # Start serving
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 Server stopped by user")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
