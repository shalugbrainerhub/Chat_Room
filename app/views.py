from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.messages import constants as messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import get_messages

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
                              Q(topic__name__icontains=q)|
                              Q(name__icontains=q)|
                              Q(description__icontains=q)
                              )
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'app/home.html', {'rooms':rooms, 'topics':topics, 'room_messages':room_messages})


def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()

    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.participants.add(request.user)

        return redirect('room', pk=room.id)


    if room is not None:  
        context={'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'app/room.html', context)


@login_required(login_url='/login')
def createRoom(request):
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=RoomForm()         
    return render(request,'app/room_form.html', {'form':form})


@login_required(login_url='/login')
def update_room(request, pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("You are not allowed here.")   
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'app/room_form.html', {'form':form})


@login_required(login_url='/login')
def delete_room(request, pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
         return HttpResponse("You are not allowed here.")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'app/delete.html', context=locals())



@login_required(login_url='/login')
def delete_message(request, pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
         return HttpResponse("You are not allowed here.")
    if request.method=='POST':
        message.delete()
        return redirect('room', message.room.id)
    return render(request, 'app/delete.html', {'obj':message})



def loginPage(request):
    page='login'
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            print("error user does not exist.")       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("User does not exist.")
    
    return render(request, 'app/login.html', {'page':page})


def logoutPage(request):
    logout(request)
    return redirect('home')

    
def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            print(form.errors)
    return render(request, 'app/login.html', {'form':form})




def userProfile(request, pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()

    return render(request, 'app/profile.html', {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics})

