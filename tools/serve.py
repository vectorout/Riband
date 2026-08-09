#!/usr/bin/env python3
"""Dev preview server for the built site. Run: python3 tools/serve.py [port]

Serves docs/ by absolute path (not cwd), so rebuilds never break it.
Port resolution: CLI arg > PORT env var (set by preview runners) > 8471.
"""
import http.server
import os
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
os.makedirs(DOCS, exist_ok=True)

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8471"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Serving {os.path.abspath(DOCS)} at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
