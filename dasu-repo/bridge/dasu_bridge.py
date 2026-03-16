"""
dasu_bridge.py  —  Dasu sheet layout tool local bridge server
=============================================================
Run with:  python dasu_bridge.py
Listens on localhost:7821

Endpoints:
  POST /receive   — Blender sends drawing payload (JSON)
  GET  /poll      — Dasu browser app fetches pending drawings
  GET  /status    — health check
  GET  /          — info page

No external dependencies — pure Python 3.6+ stdlib.
"""

import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# ── State ─────────────────────────────────────────────────────────────────────
_lock     = threading.Lock()
_drawings = []      # list of drawing dicts, newest last
_max_keep = 20      # keep last N drawings in memory

PORT = 7821
HOST = 'localhost'


# ── Request handler ───────────────────────────────────────────────────────────
class BridgeHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        ts = time.strftime('%H:%M:%S')
        print(f'  [{ts}] {fmt % args}')

    def _cors(self):
        # Allow the Dasu browser app (any localhost origin) to fetch
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/poll':
            self._poll()
        elif path == '/status':
            self._status()
        else:
            self._info()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/receive':
            self._receive()
        else:
            self._json_response(404, {'error': 'Not found'})

    # ── /receive ──────────────────────────────────────────────────────────────
    def _receive(self):
        try:
            length  = int(self.headers.get('Content-Length', 0))
            raw     = self.rfile.read(length)
            payload = json.loads(raw.decode('utf-8'))

            # Required fields
            if 'svg' not in payload:
                self._json_response(400, {'error': 'Missing svg field'})
                return

            drawing = {
                'id':          f'{int(time.time() * 1000)}',
                'receivedAt':  time.strftime('%Y-%m-%dT%H:%M:%S'),
                'name':        payload.get('name',        'Untitled'),
                'drawingName': payload.get('drawingName', ''),
                'scale':       payload.get('scale',       '1:100'),
                'scaleDenom':  payload.get('scaleDenom',  100),
                'paperMm':     payload.get('paperMm',     None),   # {w, h}
                'ifcPath':     payload.get('ifcPath',     ''),
                'projectName': payload.get('projectName', ''),
                'targetView':  payload.get('targetView',  'PLAN_VIEW'),
                'svg':         payload['svg'],
            }

            with _lock:
                _drawings.append(drawing)
                # Keep only the last N
                while len(_drawings) > _max_keep:
                    _drawings.pop(0)

            print(f'\n  ✓  Received: {drawing["name"]}  scale={drawing["scale"]}')
            self._json_response(200, {'ok': True, 'id': drawing['id']})

        except json.JSONDecodeError as e:
            self._json_response(400, {'error': f'Invalid JSON: {e}'})
        except Exception as e:
            self._json_response(500, {'error': str(e)})

    # ── /poll ─────────────────────────────────────────────────────────────────
    def _poll(self):
        """
        Returns all drawings received since `since` ms timestamp.
        Query param:  ?since=<unix_ms>   (default 0 = all)
        Dasu passes its last-seen drawing ID and only gets new ones.
        """
        from urllib.parse import parse_qs
        qs    = parse_qs(urlparse(self.path).query)
        since = qs.get('since', [''])[0]

        with _lock:
            if since:
                result = [d for d in _drawings if d['id'] > since]
            else:
                result = list(_drawings)

        self._json_response(200, {
            'drawings': result,
            'count':    len(result),
            'serverTs': int(time.time() * 1000),
        })

    # ── /status ───────────────────────────────────────────────────────────────
    def _status(self):
        with _lock:
            n = len(_drawings)
        self._json_response(200, {
            'status':   'ok',
            'port':     PORT,
            'stored':   n,
            'version':  '0.1.0',
        })

    # ── / info page ───────────────────────────────────────────────────────────
    def _info(self):
        html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Dasu Bridge</title>
<style>
  body {{ font-family: monospace; background: #1c1c1e; color: #f5f5f7;
         padding: 40px; max-width: 600px; margin: 0 auto; }}
  h1 {{ color: #30d158; }}
  .ep {{ background: #2c2c2e; padding: 10px 14px; border-radius: 6px;
         margin: 8px 0; border-left: 3px solid #30d158; }}
  .method {{ color: #0a84ff; margin-right: 8px; }}
</style></head><body>
<h1>Dasu.print Bridge  v0.1.0</h1>
<p>Local bridge between Bonsai BIM (Blender) and the Dasu sheet layout tool.</p>
<p>Listening on <strong>localhost:{PORT}</strong></p>
<h2>Endpoints</h2>
<div class="ep"><span class="method">POST</span>/receive &mdash; Blender sends drawing payload</div>
<div class="ep"><span class="method">GET</span>/poll &mdash; Dasu fetches pending drawings</div>
<div class="ep"><span class="method">GET</span>/status &mdash; Health check</div>
</body></html>'''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self._cors()
        self.end_headers()
        self.wfile.write(html.encode())

    # ── Helper ─────────────────────────────────────────────────────────────────
    def _json_response(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self._cors()
        self.end_headers()
        self.wfile.write(body)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), BridgeHandler)
    print(f'\n  Dasu Bridge  v0.1.0')
    print(f'  Listening on http://{HOST}:{PORT}')
    print(f'  Open http://{HOST}:{PORT} in your browser for info')
    print(f'\n  Waiting for drawings from Bonsai BIM...')
    print(f'  Press Ctrl+C to stop\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Bridge stopped.')
        server.server_close()
