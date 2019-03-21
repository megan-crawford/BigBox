"""BigBox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name='Main'

urlpatterns = [
    #home
	path('', views.home, name='home'),
	path('home/', views.home, name='home'),
	
    #account
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
	path('create_account/', views.create_account, name='create_account'),
    path('update_account/', views.update_account, name='update_account'),
    path('profile/', views.profile, name='profile'),
    path('generate_report/', views.generate_report, name='generate_report'),

    #creator
    path('home_creator/', views.home_creator, name='home_creator'),
    path('create_job/', views.create_job, name='create_job'),
    path('add_job/', views.new_job, name='add_job'),
    path('all_jobs_creator/', views.all_jobs_creator, name='all_jobs_creator'),
    path('accepted_jobs_creator/', views.accepted_jobs_creator, name='accepted_jobs_creator'),
    path('pending_jobs_creator/', views.pending_jobs_creator, name='pending_jobs_creator'),
    path('past_jobs_creator/', views.past_jobs_creator, name='past_jobs_creator'),

    #seeker
    path('home_seeker/', views.home_seeker, name='home_seeker'),
    path('list_job/', views.list_job, name='list_job'),
    path('all_jobs_seeker/', views.all_jobs_seeker, name='all_jobs_seeker'),
    path('accepted_jobs_seeker/', views.accepted_jobs_seeker, name="accepted_jobs_seeker"),
    path('interested_jobs_seeker/', views.interested_jobs_seeker, name='interested_jobs_seeker'),
	path('past_jobs_seeker/', views.past_jobs_seeker, name='past_jobs_seeker'),
]
