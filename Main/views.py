from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from . models import User

def register(request):
    if request.method == "POST": #user clicks register button
        form = RegisterForm(request.POST)

        if form.is_valid():
            #get form data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            location = form.cleaned_data['location']

            #create and add user to database
            user = User.objects.create(email=email, password=password,first_name=first_name, last_name=last_name, location=location)
            user.save()
            login(request, user)

            redirect('home/')
        else:
            render(request, 'Main/register.html', {'form':form})

    else: #user is viewing the register page
        form = RegisterForm()
        render(request, 'Main/register.html', {'form':form})

#home page
def home(request):
    return render(request, 'main/login.html')
    #return HttpResponse("home.")

def create_account(request):
    return render(request, 'Create Account/createAccount.html')

#redirect to home    
def logout_request(request):
    logout(request)
    redirect('home/')

#create_job page
def create_job(request):
    return render(request, 'bigBoxJob.html')
    #return HttpResponse("job.")

def list_job(request):
    return render(request, 'listJobs.html')
