from django.shortcuts import render
from .models import Room  #import room model
# from django.http import HttpResponse
# Create your views here.




def home(request):
    rooms = Room.objects.all() # Get all rooms from model
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
   

def room(request, pk):
    room = Room.objects.get(id=pk) # Get corresponding room

    
    context = {'room': room}
    return render(request, 'base/room.html', context)