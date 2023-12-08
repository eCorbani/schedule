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


@login_required(login_url='/login/')
def event(request):
    event_id = request.GET.get('id')
    data = {}
    if event_id:
        data['event'] = Event.objects.get(id=event_id)
    return render(request, 'event.html', data)


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title')
        event_date = request.POST.get('event_date')
        description = request.POST.get('description')
        location = request.POST.get('location')
        user = request.user
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            if event.user == user:
                event.title = title
                event.event_date = event_date
                event.description = description
                event.location = location
                event.save()
            '''
            Event.objects.filter(id=event_id).update(title=title,
                                                     event_date=event_date,
                                                     description=description,
                                                     location=location)
            '''
        else:
            Event.objects.create(title=title,
                                 event_date=event_date,
                                 description=description,
                                 location=location,
                                 user=user)

    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, event_id):
    user = request.user
    filtered_event = Event.objects.get(id=event_id)
    if user == filtered_event.user:
        filtered_event.delete()
    return redirect('/')
