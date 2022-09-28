import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Room, Topic, Message, Topic, TopicColor  # import room model
from .forms import RoomForm, TopicForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.core.paginator import Paginator


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
    form = UserCreationForm()  # skicka med django default sign-up form
    if request.method == 'POST':  # kontrollera validation
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Användarnamn finns inte')

        form = UserCreationForm(request.POST)
        if form.is_valid():
            # kolla att det är lowercase innan skicka till databas
            user = form.save(commit=False)
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
    )  # visa resultat om de innehåller sökresultat
    # Get all rooms from model

    # pagination
    p = Paginator(rooms, 10)
    page = request.GET.get('page')
    room_list = p.get_page(page)

    # print(len(room_list))
    # print(room_list)
    print(p.count)
    print(p.num_pages)
    print(page)

    if not page:
        page = 0

    if p.num_pages >= 4:
        bigRight = int(p.num_pages)

        if p.num_pages >= 5:
            increment = 5
            if p.num_pages >= 30:
                increment = 10
                if p.num_pages >= 50:
                    increment = 20
            bigRight = int(page) + increment
            smallLeft = int(page) - increment

        if bigRight >= int(p.num_pages):

            bigRight = int(p.num_pages)
            if int(page) == int(p.num_pages) - 1:
                bigRight = False

        if smallLeft <= 1:
            smallLeft = 1
        if int(page) <= 2:
            smallLeft = False

    else:
        bigRight = False
        smallLeft = False

    topics = Topic.objects.all()[0:30]
    room_count = rooms.count()
    # visa bara de meddelanden i side-bar som stämmer överäns med sökning (football, gaming etc)
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:5]

    context = {
        'oldrooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'rooms': room_list,
        'bigRight': bigRight,
        'smallLeft': smallLeft,


    }

    return render(request, 'base/home.html', context)


def alltopics(request):
    topics = Topic.objects.all()
    # pagination
    p = Paginator(topics, 30)
    page = request.GET.get('page')
    topics_list = p.get_page(page)

    if not page:
        page = 0

    if p.num_pages >= 4:
        bigRight = int(p.num_pages)

        if p.num_pages >= 5:
            increment = 5
            if p.num_pages >= 30:
                increment = 10
                if p.num_pages >= 50:
                    increment = 20
            bigRight = int(page) + increment
            smallLeft = int(page) - increment

        if bigRight >= int(p.num_pages):

            bigRight = int(p.num_pages)
            if int(page) == int(p.num_pages) - 1:
                bigRight = False

        if smallLeft <= 1:
            smallLeft = 1
        if int(page) <= 2:
            smallLeft = False

    else:
        bigRight = False
        smallLeft = False

    context = {
        'topics': topics_list,
        'bigRight': bigRight,
        'smallLeft': smallLeft,
    }
    return render(request, 'base/alltopics.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)  # Get corresponding room
    roomMessages = room.message_set.all()  # få alla meddelanden tillhörande tråden

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'roomMessages': roomMessages}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def userProfile(request, pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    # pagination
    p = Paginator(rooms, 10)
    page = request.GET.get('page')
    room_list = p.get_page(page)

    if not page:
        page = 0

    if p.num_pages >= 4:
        bigRight = int(p.num_pages)

        if p.num_pages >= 5:
            increment = 5
            if p.num_pages >= 30:
                increment = 10
                if p.num_pages >= 50:
                    increment = 20
            bigRight = int(page) + increment
            smallLeft = int(page) - increment

        if bigRight >= int(p.num_pages):

            bigRight = int(p.num_pages)
            if int(page) == int(p.num_pages) - 1:
                bigRight = False

        if smallLeft <= 1:
            smallLeft = 1
        if int(page) <= 2:
            smallLeft = False

    else:
        bigRight = False
        smallLeft = False

    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'oldrooms': rooms,
        'rooms': room_list,
        'topics': topics,
        'room_messages': room_messages,
        'bigRight': bigRight,
        'smallLeft': smallLeft,

    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':  # When a form is recieved, check validation
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user  # sätt host
            room.save()
            return redirect('home')  # send user back to home page

    context = {'form': form}  # pass in the form forms.py to display
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)  # Get room data with pk submited
    form = RoomForm(instance=room)  # load data in form

    if request.user != room.host:  # Meddela om man inte äger tråden man försöker ändra
        return HttpResponse('Du äger inte denna tråd')

    if request.method == 'POST':  # when form is submited check validation
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()  # override old form
            return redirect('home')  # send user home

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)  # get correct room
    if request.user != room.host:  # Meddela om man inte äger tråden man försöker ändra
        return HttpResponse('Du äger inte denna tråd')

    if request.method == 'POST':
        room.delete()  # delete
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)  # get correct room
    if request.user != message.user:  # Meddela om man inte äger meddelandet man försöker ändra
        return HttpResponse('Du äger inte denna kommentar')

    if request.method == 'POST':
        message.delete()  # delete
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


colorList = [
    '#FFF5E4',
    '#FFE3E1',
    '#FFD1D1',
    '#FF9494',
    '#B1B2FF',
    '#AAC4FF',
    '#D2DAFF',
    '#CDF0EA',
    '#ECC5FB',
    '#FAF4B7',
    '#ECC5FB',
    '#A7D2CB',
    '#F2D388',
    '#F675A8',
    '#FFCCB3',
    '#F29393',
    '#FFB3B3',
    '#FFE9AE',
    '#C1EFFF',
    '#B2C8DF',
    '#C4DFAA',  # ss
    '#F2D7D9',
    '#D3CEDF',
    '#CDF0EA',
    '#9ADCFF',
    '#B4CFB0',
    '#C3DBD9',
    '#FDCEB9',
    '#FFEFEF',
    '#EEC373',
    '#96C7C1',
    '#FFDEFA',
    '#C6D57E',
]


def topicsPage(request):
    form = TopicForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            topic = form.save(commit=False)
            topic.color = random.choice(colorList)
            topic.save()
            return redirect('home')

    context = {'TopicForm': TopicForm}
    return render(request, 'base/topics.html', context)
