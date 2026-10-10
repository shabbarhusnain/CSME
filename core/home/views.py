from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
User=get_user_model()
# Create your views here.


def login_page(request):
    if request.method=="POST":
        data= request.POST
        email= data.get('email')
        password=data.get('password')
        if not User.objects.filter(email=email).exists():
            messages.info(request,'Email dosenot Exists.')
            return redirect('/login/')
        user=authenticate(email=email, password=password)
        if user is None:
            messages.info(request,'Invalid Password.')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/home/')
    return render(request,'login.html')

def register_page(request):
    if request.method=="POST":
        data= request.POST
        email= data.get('email')
        password=data.get('password')
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email is already registered.')
            return redirect('/register/')
        user=User.objects.create(
            email=email
        )
        user.set_password(password)
        user.save()
        return redirect('/home/')
    return render(request,'register.html')
@login_required(login_url='/login/')
def home(request):
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        email=data.get('email')
        image=request.FILES.get('image')
        if UserProfile.objects.filter(email=email).exists():
            messages.info(request,'Email already Exists')
            return redirect('/home/')
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
@login_required(login_url='login/')
def send_email(request):
    if request.method=="POST":
        data=request.POST
        subject=data.get('subject')
        body=data.get('message')
        file=request.FILES.get('file')
        from_email=settings.DEFAULT_FROM_EMAIL   
        to=list(UserProfile.objects.values_list('email', flat=True))
        email=EmailMessage(
            subject=subject,body=body,from_email=from_email, to=to
        )
        email.attach(file.name,file.read(),file.content_type)
        email.send()
        messages.info(request,'Email Sent Successfully')
        return redirect('/home/')
    return render(request, 'send_email.html')
@login_required(login_url='login/')
def logout_page(request):
    logout(request)
    return redirect('/login/')

def reset_page(request):
    if request.method=="POST":
        email=request.POST.get('email')
        user=User.objects.get(email=email)
        if not User.objects.filter(email=email).exists():
            messages.info(request,"User does not exists.")
            return redirect('/reset_page/')
        else:
            email=user.email
            return redirect(f'/forget_page/{email}/')
    return render(request, 'reset_page.html')
def forget_page(request, email):
    user=User.objects.get(email=email)
    if request.method=="POST":
        passwod1=request.POST.get('password1')
        passwod2=request.POST.get('password2')
        if passwod1 != passwod2 and passwod2 != passwod1:
            messages.info(request,'Password doesnot match.')
            return redirect(f'/forget_page/{email}')
        user.set_password(passwod1)
        user.save()
        return redirect('/login/')
    return render(request, 'forget_page.html')