from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from core.models import Event


# Create your views here.

# def index(request):
#     return redirect('/schedule/')

def user_login(request):
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    return redirect('/')


@login_required(login_url='/login/')
def events_list(request):
    user = request.user
    events = Event.objects.filter(user=user)
    data = {'events': events}

    return render(request, 'schedule.html', data)
