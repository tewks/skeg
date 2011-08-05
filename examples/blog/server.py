from diesel import Application, Service, Loop 
from diesel.logmod import Logger
from diesel.protocols import http
from skeg.models import Blog
from static import static_http
import time

def json_headers(length):
    headers = http.HttpHeaders()
    headers.add('Content-Type', 'application/json')
    headers.add('Content-Length', length)
    return headers

def handle_http(req):
    if req.method == 'GET': 
        path = req.url.split('/')
        if path[1] == 'posts':
            t0 = time.time()
            posts = Blog('interiors').posts_json()
            print time.time() - t0
            return http.http_response(req, 200, json_headers(len(posts)), posts)
        else:         
    	    return static_http('static', req)

def main():
    global logger
    logger = Logger()
    app = Application()
    app.add_service(Service(http.HttpServer(handle_http), 80))
    app.run()

if __name__ == '__main__':
    main()
