from gevent import monkey
monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer

from realtime import PointerNamespace
    
class Application(object):
    def __init__(self):
        self.buffer = []
        # Dummy request object to maintain state between Namespace
        # initialization.
        self.request = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')
        
        if path.startswith('static/') or path == 'index.html':
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/pointer': PointerNamespace}, self.request)
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<a href="index.html">Go Here!</a>']


if __name__ == '__main__':
    print 'Listening on port 8000 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8000), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()