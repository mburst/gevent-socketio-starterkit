from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from collections import defaultdict
import redis

from gevent import Greenlet

def home_redis_worker():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    tacosub = r.pubsub()
    tacosub.subscribe('tacos')
    for item in tacosub.listen():
        if item['type']  == "message":
            for socket in HomeNamespace.sockets:
                socket.emit('taco', item['data'])
            
            
home_greenlet = Greenlet.spawn(home_redis_worker)


@namespace('/home')
class HomeNamespace(BaseNamespace):
    sockets = set([])
    
    def initialize(self):
        HomeNamespace.sockets.add(self)
        
    def recv_disconnect(self):
        HomeNamespace.sockets.discard(self)
        self.disconnect(silent=True)
###########################       
def user_redis_worker():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    usersub = r.pubsub()
    usersub.psubscribe('user_*')
    for item in usersub.listen():
        if item['type']  == "pmessage":
            user = item['channel'][5:]
            for socket in UserNamespace.sockets[user]:
                socket.emit('taco', item['data'])
            
            
user_greenlet = Greenlet.spawn(user_redis_worker)


@namespace('/user')
class UserNamespace(BaseNamespace):
    sockets = defaultdict(set)
    
    def on_set_user(self, username):    
        self.username = username
        UserNamespace.sockets[username].add(self)
        
    def recv_disconnect(self):
        UserNamespace.sockets[self.username].discard(self)
        self.disconnect(silent=True)