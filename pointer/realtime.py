from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin


class PointerNamespace(BaseNamespace, BroadcastMixin):
    user_count = 0

    def recv_connect(self):
        # in this case 'self' is the socket connection
        PointerNamespace.user_count += 1
        self.broadcast_event('update_count', PointerNamespace.user_count)

    def recv_disconnect(self):
        PointerNamespace.user_count -= 1
        self.broadcast_event('update_count', PointerNamespace.user_count)

        super(PointerNamespace, self).recv_disconnect()
        # handled by super() above
        #self.disconnect(silent=True)  # silent=True will not send a disconnect packet to the client

    def on_moved(self, coordinates):
        print 'moved: {}'.format(coordinates)
        self.broadcast_event_not_me('move', {
            'user': self.user,
            'x': coordinates['x'],
            'y': coordinates['y'],
        })

    @property
    def user(self):
        return '-' + self.socket.sessid  # CSS IDs cannot start with numbers so prefix
