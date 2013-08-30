from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
#from socketio.mixins import RoomsMixin, BroadcastMixin

#from collections import defaultdict
#import threading

@namespace('/home')
class HomeNamespace(BaseNamespace):
    sockets = set([])    
    
    def initialize(self):
        self.sockets.add(self)
                
    def recv_disconnect(self):
        self.sockets.discard(self)
        self.disconnect(silent=True)