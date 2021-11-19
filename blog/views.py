from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.db.models import Q
from .forms import RoomForm, register, Profile


# Create your views here.
def home(request):
    room=Topic.objects.all()
    profile=Imager.objects.all()
    q=request.GET.get('q') if request.GET.get('q') else ''
    a=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ).order_by('-created')
    return render(request,'blog/home.html',{'room':room,'a':a,'p':profile})

def signup_form(request):
    user=register()
    if request.method=='POST':
        user=register(request.POST)
        if user.is_valid():
            user.save()
            return redirect('home')
    return render(request,'blog/sign.html',{'user':user})


def login_form(request):
    if request.method=="POST":
        name=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=name)
        except:
            messages.error(request,'user not exist please check agin')
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username and password not exist')
    return render(request,'blog/login.html')

def room_page(request,pk):
    a=Room.objects.get(id=pk)
    room=Topic.objects.all()
    profile=Imager.objects.filter(user=a.host).first()
    b=a.message_set.all().order_by('-created')
    if request.method=='POST':
        body=request.POST.get('body')
        b = Message.objects.create( user=request.user,body=body,room=a)
        return redirect('room_page',pk=a.id)
    return render(request,'blog/room_page.html',{'a':a,"b":b,'profile':profile})



@login_required(login_url='login/')
def logout_user(request):
    logout(request)
    return redirect('home')

def edit(request,pk):
    a=Room.objects.get(id=pk)
    b=RoomForm(instance=a)
    if request.method=='POST':
        b=RoomForm(request.POST,instance=a)
        if b.is_valid():
            b.save()
            return redirect('home')
    return render(request,'blog/edit.html',{'b':b})



@login_required(login_url='login/')
def delete_post(request,pk):
    a=Room.objects.get(id=pk)
    if request.method=="POST":
        a.delete()
        return redirect('home')
    return render(request,'blog/delete.html')


@login_required(login_url='login')
def create_post(request):
    a=RoomForm()
    if request.method=='POST':
        a=RoomForm(request.POST)
        if a.is_valid():
            host=a.save(commit=False)
            host.host=request.user
            host.save()
        
            
            return redirect('home')
    return render(request,'blog/create.html',{'a':a,'name':request.user})

@login_required(login_url='login')
def profile(request,pk):
    d=Room.objects.get(id=pk)
    a=User.objects.get(username=d.host)
    b=Profile(instance=a)
    if request.method=="POST":
        b=Profile(request.POST,request.FILES,instance=a)
        if b.is_valid():
            b.save()
            return redirect('profile',pk=a)
        
    c=Imager.objects.filter(user=d.host).first()
    return render(request,'blog/profile.html',{'a':b,'c':c})


