from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth import login, logout
from . models import Users

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
            user = Users.objects.create(email=email, password=password,first_name=first_name, last_name=last_name, location=location)
            user.save()
            login(request, user)

            redirect('home/')
        else:
            render(request, 'Main/register.html', {'form':form})

    else: #user is viewing the register page
        form = RegisterForm()
        render(request, 'Main/register.html', {'form':form})