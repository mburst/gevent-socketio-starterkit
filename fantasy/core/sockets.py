from core.models import *

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

import logging
import redis

from collections import defaultdict
def nested_defaultdict():
    return defaultdict(dict)

@namespace('/home')
class HomeNamespace(BaseNamespace, BroadcastMixin):
    
    def initialize(self):
        '''self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")'''
    
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
    
    def on_create_league(self, league_name):
        league = League.objects.create(name=league_name)
        self.broadcast_event('new_league', {'id': league.id, 'name': league.name})
                
    #Try and join a league by making sure that it exists and that it is not full
    def on_join_league(self, league_info):
        try:
            league = League.objects.get(id=league_info['league_id'])
        except Exception, e:
            self.error('Bad League ID', 'Unable to join the specified league. Please try again')
            return
        
        if not league.locked:
            team = Team.objects.create(name=league_info['team_name'], league=league, owner=self.request.user)
            self.broadcast_event_not_me('new_member', {'full': league.full(), 'league_id': league.id, 'team_name': team.name})
            self.emit('redirect', league.get_draft_url())
        else:
            self.error('Locked', 'That league is currently full')
    
                
@namespace('/draft')
class DraftNamespace(BaseNamespace, RoomsMixin):    
    drafts = defaultdict(nested_defaultdict) 
    
    def initialize(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    #Loads when our client connects. Lists all default methods client has access to
    def get_initial_acl(self):
        return ['on_join', 'recv_connect', 'recv_disconnect']
    
    def recv_disconnect(self):
        del self.drafts[self.league.id]['sockets'][self.team.id]
        self.disconnect(silent=True)
    
    #The rooms mixin loops through each socket and checks if it has access to the room
    #This just emits to only the sockets in our league so it's more efficient
    #I've left the commented out rooms code for comparison though
    def emit_to_league(self, league_id, event, msg):
        for socket in self.drafts[league_id]['sockets'].itervalues():
            socket.emit(event, msg)
    
    def on_join(self, league_id):
        #self.join('draft_' + league_id)
        self.league = League.objects.get(id=league_id)
        self.team = Team.objects.get(league=league_id, owner=self.request.user)
        league_id = int(league_id)
        self.drafts[league_id]['sockets'][self.team.id] = self
        self.emit_to_league(league_id, 'new_team', {'id': self.team.id, 'name': self.team.name})
        
        #Check if we've reconnected and it's our pick
        current_pick = self.drafts[self.league.id].get('current_pick')
        if current_pick == self.team.id:
            self.drafts[self.league.id]['sockets'][current_pick].add_acl_method('on_pick')
        
        #Start the draft now that everyone is here
        if len(self.drafts[league_id]['sockets']) == 4 and self.league.locked == False:
            self.league.locked = True
            self.league.save()
            self.league.generate_draft_order()
            self.drafts[league_id]['current_pick'] = ''
            self.pick_logic()
        
    def on_pick(self, player_id):
        player = Player.objects.get(id=player_id)
        self.team.players.add(player)
        #self.emit_to_room('draft_' + str(self.league.id), 'player_drafted', {'player': player_id, 'team': self.team.id})
        self.emit_to_league(self.league.id, 'player_drafted', {'player': player_id, 'team': self.team.id})
        self.pick_logic()
        
    def pick_logic(self):
        current_pick = self.drafts[self.league.id].get('current_pick')
        #Delete pick method access from person who just picked
        if current_pick:
            self.drafts[self.league.id]['sockets'][current_pick].del_acl_method('on_pick')
        #Grab next drafer. This list is sent to redis from the models.py
        drafter = self.r.lpop('draft_order_' + str(self.league.id))
        
        #Set the current pick and give the socket access to the on_pick method
        #lpop will return none if there aren't anymore drafters in the list
        #So when it equals none we emit the draft_over event
        if drafter:
            drafter = int(drafter)
            self.drafts[self.league.id]['current_pick'] = drafter
            self.drafts[self.league.id]['sockets'][drafter].add_acl_method('on_pick')
            #self.emit_to_room('draft_' + str(self.league.id), 'new_drafter', self.drafts[self.league.id]['sockets'][drafter].team.name)
            self.emit_to_league(self.league.id, 'new_drafter', self.drafts[self.league.id]['sockets'][drafter].team.name)
        else:
            self.emit_to_league(self.league.id, 'draft_over', "The Draft is now over!")