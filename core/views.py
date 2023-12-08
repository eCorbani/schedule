from django.shortcuts import render, redirect
from core.models import Event


# Create your views here.

# def index(request):
#     return redirect('/schedule/')


def events_list(request):
    user = request.user
    events = Event.objects.filter(user=user)
    data = {'events': events}

    return render(request, 'schedule.html', data)
