from core.models import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@login_required
def home(request):
    leagues = League.objects.filter(locked=False)
    my_teams = Team.objects.filter(owner=request.user)
    return render(request, 'index.html', locals())

@login_required
def draft(request, league_id):
    teams = Team.objects.filter(league=league_id).prefetch_related('players')
    drafted_ids = []
    for team in teams:
        if team.owner == request.user:
            team_name = team.name
        for player in team.players.all():
            drafted_ids.append(player.id)
    
    remaining_players = Player.objects.exclude(id__in=drafted_ids)
    return render(request, 'draft.html', locals())

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            try:
                new_user = authenticate(username=new_user.username, password=request.POST['password2'])
                if new_user is not None:
                    login(request, new_user)
            except:
                pass
            return redirect('home')
    
    return render(request, 'register.html', locals())