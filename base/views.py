from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# rooms = [
#     {"id": 1, "name": "Room 1"},
#     {"id": 2, "name": "Room 2"},
#     {"id": 3, "name": "Room 3"},
# ]


def home(request):
    q = request.GET.get("q") if request.GET.get("q") else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context)


def room(request, name):
    room = Room.objects.get(id=name)
    context = {"room": room}
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            room = form.save(commit=False)
            if room.host != request.user:
                messages.error(request, "You aren't authorized to create this room")
                return redirect("home")
            else:
                form.save()
                return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, name):
    room = Room.objects.get(id=name)
    form = RoomForm(request.POST or None, instance=room)

    if request.user != room.host:
        return HttpResponse("You are not authorized to update this room")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, name):
    room = Room.objects.get(id=name)
    if request.user != room.host:
        return HttpResponse("You are not authorized to delete this room")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context)


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.info(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User created successfully")
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("register")
    context = {"form": form}
    return render(request, "base/login_register.html", context)
