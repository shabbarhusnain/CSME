from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from .models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
User=get_user_model()
# Create your views here.


def login_page(request):
    if request.method=="POST":
        data= request.POST
        email= data.get('name')
        password=data.get('password')
        if not AdminPanel.objects.filter(email=email).exists():
            messages.info(request,'Email dosenot Exists.')
            return redirect('/login/')
        admin=authenticate(email=email, password=password)
        if admin is None:
            messages.info(request,'Invalid Password.')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/home/')
    return render(request,'login.html')

def register_page(request):
    if request.method=="POST":
        data= request.POST
        email= data.get('name')
        password=data.get('password')
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email is already registered.')
            return redirect('/register/')
        user=User.objects.create(
            email=email
        )
        user.set_password(password)
        user.save()
        return redirect('/home')
    return render(request,'regster.html')

def home(request):
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        email=data.get('email')
        image=request.FIELE.get('image')
        UserProfile.objects.create(
            user=request.user,
            name=name,
            email=email,
            image=image
        )
        return redirect('/home/') 
    userprofiles=UserProfile.objects.all()
    history=ProfileHistory.objects.all()

    context={
        'userprofiles':userprofiles,
        'history':history
    }
    return render(request,'home.html',context)
def send_email(request):
    if request.method=="POST":
        data=request.POST
        subject=data.get('subject')
        body=data.get('message')
        file=request.FILES.get('file')
        from_email=settings.EMAIL_HOST_USER
        users= User.objects.all()
        to=users.email
        email=EmailMessage(
            subject=subject,body=body,from_email=from_email, to=to
        )
        email.attach(file.read,file.read(),file.content_type)
        email.send()
        messages.info(request,'Email Sent Successfully')
        return redirect('/home/')
    return render(request, 'send_email.html')
def logout_page(request):
    logout(request)
    return redirect('/login/')