from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import CreateAccountForm, LoginForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from . models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

def create_account(request):
    if request.method == "POST": #user clicks register button
        form = CreateAccountForm(request.POST)

        print('create account post')
        #print(form.cleaned_data.get('first_name'))

        if form.is_valid():
            print('create account valid')

            #get form data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']

            #create and add user to database
            user = User.objects.create(Email=email, Password=password, FirstName=first_name, LastName=last_name, Age=age)
            user.save()
            login(request, user)
            
            return redirect('home/')
        else:
            print('create account not valid')
            return render(request, 'createAccount.html', {'form':form})

    else: #user is viewing the create account page
        print('create account non post')

        form = CreateAccountForm()
        return render(request, 'createAccount.html', {'form':form})
        #redirect('create_account/')

def profile(request):
    return render(request, 'profile.html')
    #return HttpResponse("profile.")

def update_account(request):
    return render(request, 'updateAccount.html')
    #return HttpResponse("update_account")

#home page
def home(request):
    return render(request, 'home.html')
    #return HttpResponse("home.")

def login_request(request):
    if request.method == 'POST': #user clicks submit -> check form info
        print('login post')
        form = LoginForm(request.POST)

        if form.is_valid():
            print('login valid')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print('email: ', email)
            print('password: ', password)

            user = authenticate(Email=email, password=password)
            if user is not None:
                print('login user found')
                login(request, user)

                if request.user.is_authenticated():
                    print("Logged in")
                else:
                    print("Not logged in")

                return redirect('/')
            else:
                form.add_error(None, LoginForm.error_messages['invalid_login'])

        #else not valid -> send form with error details

    else: #user opens page -> send blank form
        print('login non post')
        form = LoginForm()

    return render(request, 'login.html', {'form':form})

#redirect to home    
def logout_request(request):
    logout(request)
    return redirect('home/')

#create_job page
def create_job(request):
    return render(request, 'Jobs/bigBoxJob.html')
    #return HttpResponse("job.")

def list_job(request):
    return render(request, 'Jobs/listJobs.html')

@csrf_exempt
def new_job(request):
    return render(request, 'Jobs/viewNewJob.html')
