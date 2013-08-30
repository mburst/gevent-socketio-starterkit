from core.models import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    tacos = Taco.objects.order_by('-id')[:20]
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

def user_profile(request, username=None):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = TacoForm(request.user, request.POST)
        if form.is_valid():
            form = form.save()
    form = TacoForm(request.user)
    tacos = Taco.objects.filter(user=user)[:20]
    return render(request, 'user_profile.html', locals())