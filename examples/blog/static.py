'''Very simple static web server.

https://github.com/jamwt/diesel/blob/master/examples/dhttpd
'''
import os
import mimetypes

from diesel import Application, Service, log
from diesel.protocols import http

DEFAULT_FILE = "index.html"

def static_http(base, req):
    ct = 'text/plain'
    if req.method != 'GET':
        content = 'Method unsupported'
        code = 501
    else:
        assert '..' not in req.url, "Very basic security..."
        path = (req.url + DEFAULT_FILE) if req.url.endswith('/') else req.url
        serve_path = os.path.join(base, path[1:])
        if not os.path.exists(serve_path):
            code = 404
            content = 'Not found'
        else: 
            try: 
                content = open(serve_path, 'rb')
            except IOError:
                content = 'Permission denied'
                code = 403          
            else:                   
                code = 200
                ct = mimetypes.guess_type(serve_path)[0] or 'application/octet-stream'
   
    headers = http.HttpHeaders()
    if type(content) in (str, unicode):
        headers.add('Content-Length', len(content))
    else:
        headers.add('Connection', 'close')

    headers.add('Content-Type', ct)
    return http.http_response(req, code, headers, content)
