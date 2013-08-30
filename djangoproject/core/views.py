from core.models import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

#import redis
#r = redis.StrictRedis(host='localhost', port=6379, db=0)

def home(request):
    return render(request, 'index.html', locals())

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