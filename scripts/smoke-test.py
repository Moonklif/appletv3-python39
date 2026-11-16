#!/usr/bin/env python3
"""Run on Apple TV. Test imports and an ephemeral loopback HTTP endpoint."""
import importlib
import platform
import sys
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

assert sys.version_info[:3] == (3, 9, 25), sys.version
print(sys.version)
print(platform.platform(), platform.machine())
for name in ('json', 'socket', 'asyncio', 'http.server', 'sqlite3', 'zlib', 'bz2', 'pyexpat'):
    importlib.import_module(name)
    print('PASS import', name)
import sqlite3
print('SQLite', sqlite3.sqlite_version)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'appletv3-python39\n')
server = HTTPServer(('127.0.0.1', 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    with urllib.request.urlopen('http://127.0.0.1:%d/' % server.server_port, timeout=5) as response:
        assert response.status == 200
        assert response.read() == b'appletv3-python39\n'
    print('PASS loopback HTTP 200')
finally:
    server.shutdown()
    thread.join()
    server.server_close()
