from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Room, Topic, Message#import room model
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm




def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # kolla om användare finns - annars visa felmedelande
        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request, 'Användarnamn finns inte')
        
        user = authenticate(request, username=username, password=password)
        # logga in användare och skicka tillbaka till förstasidan
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Användarnamn finns inte')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm() # skicka med django default sign-up form
    if request.method == 'POST': # kontrollera validation
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # kolla att det är lowercase innan skicka till databas
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Användarnamnet är ogiltigt')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.all() 
 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q) 
        ) # visa resultat om de innehåller sökresultat
    # Get all rooms from model
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) # visa bara de meddelanden i side-bar som stämmer överäns med sökning (football, gaming etc)
    context = {
        'rooms': rooms,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages
        }

    return render(request, 'base/home.html', context)
   

def room(request, pk):
    room = Room.objects.get(id=pk) # Get corresponding room
    roomMessages = room.message_set.all() # få alla meddelanden tillhörande tråden

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'roomMessages': roomMessages}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user':user,
        'rooms':rooms,
        'topics': topics,
        'room_messages': room_messages
        }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST': # When a form is recieved, check validation
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user # sätt host 
            room.save()
            return redirect('home') # send user back to home page

    context = {'form': form} # pass in the form forms.py to display
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # Get room data with pk submited
    form = RoomForm(instance=room) # load data in form

    if request.user != room.host: # Meddela om man inte äger tråden man försöker ändra
        return HttpResponse('Du äger inte denna tråd')

    if request.method == 'POST': # when form is submited check validation
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save() # override old form
            return redirect('home') # send user home

    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) # get correct room
    if request.user != room.host: # Meddela om man inte äger tråden man försöker ändra
        return HttpResponse('Du äger inte denna tråd')


    if request.method == 'POST':
        room.delete() # delete
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk) # get correct room
    if request.user != message.user: # Meddela om man inte äger meddelandet man försöker ändra
        return HttpResponse('Du äger inte denna kommentar')


    if request.method == 'POST':
        message.delete() # delete
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


