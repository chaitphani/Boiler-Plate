from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.forms import ModelForm
from Auth_app.models import Regmodel
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from random import randint
from django.core.mail import EmailMessage
from ReadyTo_project import settings
from django.core.mail import send_mail


class RegmodelForm(ModelForm):
    class Meta:
        model = Regmodel
        fields = '__all__'

def is_authorized(func):
    def wrap(request, *args, **kwargs):
        try:
            login_user = Regmodel.objects.get(id=request.session['pk'])
        except:
            login_user = False
        if 'pk' in request.session.keys() and login_user:
            return func(request, *args, **kwargs)
        request.session.clear()
        return redirect('index')
    return wrap

@is_authorized
def dashboard(request):
    return render(request, 'base.html', {})


def index(request):
    return render(request, 'index.html', {})


def signup(request):
    form = RegmodelForm(request.POST or None)
    # try:
    if form.is_valid():
        pwd = form.save(commit=False)
        pwd.password = make_password(request.POST['password'])
        pwd.confirm_password = make_password(request.POST['confirm_password'])
        pwd.save()
        return redirect('login')
    return render(request, 'signup.html', {'form': form})

@is_authorized
def retrieve(request):
    visible = Regmodel.objects.all()
    return render(request, 'retrieve.html', {'visible': visible})

@is_authorized
def updation(request, pk):
    logs = get_object_or_404(Regmodel, pk=pk)
    form = RegmodelForm(request.POST or None, instance=logs)
    if form.is_valid():
        pwd = form.save(commit=False)
        pwd.password = make_password(request.POST['password'])
        pwd.save()
        return redirect('retrieve')
    return render(request, 'signup.html', {'form': form})


def deletion(request):
    try:
        del request.session['pk']
    except:
        pass
    return redirect('login')

def login(request):
    if request.method == 'POST':
        usrname = request.POST['usrname']
        password = request.POST['password']
        try:
            user = Regmodel.objects.get(usrname=usrname)
            request.session['pk'] = user.pk
            request.session['mobile'] = user.mobile
        except:
            user = False
            messages.error(request, 'Invalid User Name')
            return redirect('login')
        match = check_password(password, user.password)
        if match:
            print('success')
            return redirect('dashboard')
        else:
            print("Invalid password")
            messages.error(request, 'Invalid Password')
            return redirect('login')
    return render(request, 'login.html')

# def success(request):
#     return render(request, 'success.html', {})


def logout(request):
    try:
        del request.session['pk']
        del request.session['mobile']
    except:
        pass
    return redirect('index')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = Regmodel.objects.get(email=email)
        except:
            user = False
        if user:
            request.session['id'] = user.id
            otp = randint(1000, 99999)
            print(otp)
            request.session['otp'] = otp
            subject = 'forgotten password'
            message = 'make sure not to share your otp with anyone' + str(otp)
            email = 'chaitanyaphanikanth@gmail.com'
            emails = EmailMessage(subject, message, [email],)
            emails.send()
            return redirect('otp')
        else:
            messages.error(request, 'enter a registered email')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html', {})


def otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        if int(request.session['otp']) == int(otp):
            return redirect('reset_password')
        else:
            messages.error(request, 'invalid OTP, try again')
            return redirect('otp')
    return render(request, 'otp.html', {})


def reset_password(request):
    rocks12 = Regmodel.objects.get(id=request.session['id'])
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            rocks12.password = make_password(password)
            rocks12.save()
            return redirect('login')
        else:
            messages.error(request, 'password mis match')
            return redirect('reset_password')
    return render(request, 'reset_password.html', {})
