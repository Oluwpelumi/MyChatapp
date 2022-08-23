from email import message
from pyexpat.errors import messages
import re
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message

# Create your views here.


def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {'username':username, 'room':room, 'room_details':room_details})


def check(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

    

def send(request):
    username = request.POST['username']
    message = request.POST['message']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(user=username, value=message, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})