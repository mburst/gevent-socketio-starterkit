from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

class PointerNamespace(BaseNamespace, BroadcastMixin):
    user_count = 0
    
    def recv_connect(self):
        PointerNamespace.user_count += 1
        self.broadcast_event('update_count', PointerNamespace.user_count)
    
    def on_moved(self, coordinates):
        print coordinates
        self.broadcast_event_not_me('move', {"user": '_' + self.socket.sessid, "x": coordinates['x'], "y": coordinates['y']})
        
    def recv_disconnect(self):
        PointerNamespace.user_count -= 1
        self.broadcast_event('update_count', PointerNamespace.user_count)
        self.disconnect(silent=True)