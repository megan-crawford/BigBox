from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.http import HttpResponse
from . forms import CreateAccountForm, UpdateAccountForm, CreateJobForm, ListJobsForm, GenerateReportForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from . models import Profile, Post, Seeker, Creator, Report
from django.core.mail import EmailMessage, send_mail
from django.core.exceptions import ValidationError
from django.template import loader #?
from django.db.models import Q #for Django OR filters
from django.db.models.fields import BLANK_CHOICE_DASH

def create_account(request):
    if request.method == "POST": #user clicks register button
        #print('create account post')

        print("Attempt CreateAccount")
        try:
            form = CreateAccountForm(request.POST)
        except:
            print("oh no")
            #print(e)

        if form.is_valid():
            print('Create Account Valid')

            #get form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']

            #create and add user to database
            user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            Profile.objects.create(User=user, Age=age)
            Seeker.objects.create(User=user)
            Creator.objects.create(User=user)

            user.save()

            login(request, user)
            return redirect('/home_seeker/')

        else:
            print("Create Account not Valid")

    else: #user is viewing the create account page
        print("Load Create Account")
        form = CreateAccountForm()

    return render(request, 'createAccount.html', {'form':form})

def profile(request):
    if request.GET.get('username'): #the .get() needs to be used to stop error if username is null
        username = request.GET['username']
        user = User.objects.filter(username=username).first() #assume there is only one object
        if user:
            num_reports = Report.objects.filter(User=user).count()
            return render(request, 'profile.html', {'user_info':user, 'num_reports':num_reports})

    return render(request, 'profile.html')

#TODO: change to update profile
def update_account(request):
    #TODO: check if user is logged in

    if request.method == 'POST':
        #print('update account post')
        form = UpdateAccountForm(request.POST)

        if form.is_valid():
            #print('update account valid')
            update_all = 'update_all_button' in request.POST

            if form.cleaned_data['profile_picture'] and ('profile_picture_button' in request.POST or update_all):
                request.user.profile.ProfilePicture = form.cleaned_data['profile_picture'] 

            if form.cleaned_data['first_name'] and ('first_name_button' in request.POST or update_all):
                request.user.first_name = form.cleaned_data['first_name']

            if  form.cleaned_data['last_name'] and ('last_name_button' in request.POST or update_all):
                request.user.last_name = form.cleaned_data['last_name']

            if form.cleaned_data['age'] and ('age_button' in request.POST or update_all):
                request.user.profile.Age = form.cleaned_data['age']

            if form.cleaned_data['email'] and ('email_button' in request.POST or update_all):
                request.user.email = form.cleaned_data['email']

            if form.cleaned_data['description'] and ('description_button' in request.POST or update_all):
                request.user.profile.Description = form.cleaned_data['description']

            if (form.cleaned_data['password'] and form.cleaned_data['password_confirmation']) and ('password_button' in request.POST or update_all):
                request.user.set_password(form.cleaned_data['password'])

            request.user.save()
            request.user.profile.save()

            return render(request, 'updateAccount.html')
    else:
        form = UpdateAccountForm()

    return render(request, 'updateAccount.html', {'form': form, 'user_info':request.user})

	#reset password
def reset_password(request):
	return render(request, 'reset_password.html')
	
#home pages
def home(request):
    return render(request, 'home.html')
    #return HttpResponse("home.")
	
def home_creator(request):
    return render(request, 'home_creator.html')
	
def home_seeker(request):
    
    return render(request, 'home_seeker.html')

def login_request(request):
    if request.method == 'POST':
        print('login post')
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            print('login valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                #print('login success')
                login(request, user)
                return redirect('/home_seeker/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form':form})

#redirect to home    
def logout_request(request):
    logout(request)
    return redirect('/home/')

#create_job page
def create_job(request):
    #TODO: check if user is logged in

    if request.method == 'POST':
        #print('create job post')
        form = CreateJobForm(request.POST)

        if form.is_valid():
            #print('create job valid')

            #get form fields
            pay = form.cleaned_data['pay']
            date = form.cleaned_data['date_time']
            description = form.cleaned_data['description']
            job_type = form.cleaned_data['job_type']

            #create new job
            post = Post.objects.create(Pay=pay, DateTime=date, Description=description, JobType=job_type)
            request.user.creator.Posts.add(post)

            return redirect('/add_job/')
    else:
        form = CreateJobForm()

    return render(request, 'Jobs/bigBoxJob.html', {'form':form})

def list_job(request):
    #TODO: check if user is logged in
    if request.method == "GET":
        #print('list job get')
        form = ListJobsForm(request.GET)

        if form.is_valid():
            #print('list job valid')
            #max_distance = form.cleaned_data['max_distance']
            job_type = form.cleaned_data['job_type']
            min_wage = form.cleaned_data['min_wage']
            max_wage = form.cleaned_data['max_wage']

            if (job_type != '' and min_wage and max_wage): #all inputs filled in
                jobs = Post.objects.filter(JobType=job_type, Pay__range=[min_wage, max_wage])
            elif (job_type == '' and not min_wage and not max_wage): #no inputs filled in
                jobs = Post.objects.all()
            else: #mixed inputs filled in
                if min_wage and not max_wage:
                    jobs = Post.objects.filter(Q(JobType=job_type) | Q(Pay__gte=min_wage))
                elif not min_wage and max_wage:
                    jobs = Post.objects.filter(Q(JobType=job_type) | Q(Pay__lte=max_wage))
                else:
                    jobs = Post.objects.filter(Q(JobType=job_type) | Q(Pay__range=[min_wage, max_wage]))
        else:
            jobs = Post.objects.all()
    else:
        jobs = Post.objects.all()
        form = ListJobsForm()

    jobs = jobs.order_by('Pay', 'DateTime')
    return render(request, 'Jobs/listJobs.html', {'form':form, 'jobs':jobs})

def new_job(request):
    return render(request, 'Jobs/viewNewJob.html')

def view_one_job(request):
    return render(request, 'Jobs/oneJob.html')

#Job Creator Pages
def all_jobs_creator(request):
    if request.method == "GET":
        print('creator job get')
        form = ListJobsForm(request.GET)

        if form.is_valid():
            print('creator job valid')

            #max_distance = form.cleaned_data['max_distance']
            job_type = form.cleaned_data['job_type']
            min_wage = form.cleaned_data['min_wage']
            max_wage = form.cleaned_data['max_wage']

            if (job_type != '' and min_wage and max_wage): #all inputs filled in
                jobs = request.user.creator.Posts.filter(JobType=job_type, Pay__range=[min_wage, max_wage])
            elif (job_type == '' and not min_wage and not max_wage): #no inputs filled in
                jobs = request.user.creator.Posts.all()
            else: #mixed inputs filled in
                if min_wage and not max_wage:
                    jobs = request.user.creator.Posts.filter(Q(JobType=job_type) | Q(Pay__gte=min_wage))
                elif not min_wage and max_wage:
                    jobs = request.user.creator.Posts.filter(Q(JobType=job_type) | Q(Pay__lte=max_wage))
                else:
                    jobs = request.user.creator.Posts.filter(Q(JobType=job_type) | Q(Pay__range=[min_wage, max_wage]))
        else:
            jobs = request.user.creator.Posts.all()
    else:
        jobs = request.user.creator.Posts.all()
        form = ListJobsForm()

    jobs = jobs.order_by('Pay', 'DateTime')
    return render(request, 'Creator/allJobsCreator.html', {'form':form, 'jobs':jobs})

def accepted_jobs_creator(request):
    return render(request, 'Creator/acceptedJobsCreator.html')

def pending_jobs_creator(request):
    if request.method == "GET":
        print('creator job get')
        form = ListJobsForm(request.GET)

        if form.is_valid():
            print('list job valid')

            #max_distance = form.cleaned_data['max_distance']
            job_type = form.cleaned_data['job_type']
            min_wage = form.cleaned_data['min_wage']
            max_wage = form.cleaned_data['max_wage']

            if (job_type != '' and min_wage and max_wage): #all inputs filled in
                jobs = request.user.creator.Posts.filter(JobType=job_type, Pay__range=[min_wage, max_wage])
            elif (job_type == '' and not min_wage and not max_wage): #no inputs filled in
                jobs = request.user.creator.Posts.all()
            else: #mixed inputs filled in
                if min_wage and not max_wage:
                    jobs = request.user.creator.Posts.filter(Q(JobType=job_type) | Q(Pay__gte=min_wage))
                elif not min_wage and max_wage:
                    jobs = request.user.creator.Posts.filter(Q(JobType=job_type) | Q(Pay__lte=max_wage))
                else:
                    jobs = request.user.creator.Posts.filter(Q(JobType=job_type) | Q(Pay__range=[min_wage, max_wage]))
        else:
            jobs = request.user.creator.Posts.all()
    else:
        jobs = request.user.creator.Posts.all()
        form = ListJobsForm()

    jobs = jobs.order_by('Pay', 'DateTime')
    return render(request, 'Creator/pendingJobsCreator.html', {'form':form, 'jobs':jobs})

def past_jobs_creator(request):
    return render(request, 'Creator/pastJobsCreator.html')

def one_job(request):
    return render(request, 'Jobs/oneJob.html')

#Jobs Seeker Pages
def all_jobs_seeker(request):
    return render(request, 'Seeker/allJobsSeeker.html')

def accepted_jobs_seeker(request):
    return render(request, 'Seeker/acceptedJobsSeeker.html')

def interested_jobs_seeker(request):
    return render(request, 'Seeker/interestedJobsSeeker.html')
	
#User Report Page
def generate_report(request):
    #check get info
    if request.GET.get('username'):
        username = request.GET.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'generate_report.html') #no form info should be displayed, it isn't needed in this case
    else:
        return render(request, 'generate_report.html')

    #process request
    if request.method == "POST":
        #print('create report post')
        form = GenerateReportForm(request.POST)

        if form.is_valid():
            #print('create report valid')
            classification = form.cleaned_data['classification']
            details = form.cleaned_data['details']
            Report.objects.create(Classification=classification, Details=details, User=user)

            return redirect('/profile/?username=' + user.username)
    else:
        form = GenerateReportForm()

    return render(request, 'generate_report.html', {'form':form, 'user_info':user})

def past_jobs_seeker(request):
    return render(request, 'Seeker/pastJobsSeeker.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


#this takes the email as a param and uses it to look for the right user to see if the email is regisetered. 
#if it is not registered then it will return -1
#otherwise it will send an email with a link to where to change the password
def change_passwordBackend(email):
    try:
        obj = User.objects.get(email = email)

    except:
        return -1

    link = ""
    message = "To reset your password go to this link: "
    message += link #add link
    sendEmail("change email", "",email)


def sendEmail(subject, message, emailTo):
    try:
        email = EmailMessage(subject, message, to=[emailTo])
        num = email.send()
    except:
        return -1
    return 1
