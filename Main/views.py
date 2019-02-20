from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import CreateAccountForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from . models import User
from django.views.decorators.csrf import csrf_exempt

def create_account(request):
    if request.method == "POST": #user clicks register button
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home/')
        else:
            return render(request, 'Create Account/createAccount.html', {'form':form})

    else: #user is viewing the create account page
        form = CreateAccountForm()
        return render(request, 'Create Account/createAccount.html', {'form':form})

#home page
def home(request):
    return render(request, 'login.html')
    #return HttpResponse("home.")

# def create_account(request):
#     return render(request, 'Create Account/createAccount.html')

#redirect to home    
def logout_request(request):
    logout(request)
    redirect('home/')

#create_job page
def create_job(request):
    return render(request, 'Jobs/bigBoxJob.html')
    #return HttpResponse("job.")

def list_job(request):
    return render(request, 'Jobs/listJobs.html')

@csrf_exempt
def new_job(request):
    return render(request, 'Jobs/viewNewJob.html')
