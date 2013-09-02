from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse

class League(models.Model):
    name = models.CharField(max_length=255)
    locked = models.BooleanField()
    size = models.IntegerField(default=4)
    
    def get_draft_url(self):
        return reverse('core.views.draft', args=[str(self.id)])
    
    def full(self):
        if self.team_set.count() == self.size:
            return True
        return False
    
    def generate_draft_order(self, rounds=2):
        import redis
        
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.delete('draft_order_' + str(self.id))
        
        teams = self.team_set.values_list('id', flat=True).order_by('?')
        snake = False
        for round in xrange(rounds):
            if snake:
                for team in teams[::-1]:
                    r.rpush('draft_order_' + str(self.id), team)
                snake = False
            else:    
                for team in teams:
                    r.rpush('draft_order_' + str(self.id), team)
                snake = True
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    league = models.ForeignKey(League)
    players = models.ManyToManyField('Player', blank=True)
    
    class Meta:
        unique_together = ('owner', 'league',)
    
class Player(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)