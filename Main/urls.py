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
from django.urls import path, reverse_lazy
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

#app_name='Main'

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
	#path('reset_password/', views.reset_password, name='reset_password'),
    
    

    #creator
    path('home_creator/', views.home_creator, name='home_creator'),
    path('create_job/', views.create_job, name='create_job'),
    path('add_job/', views.new_job, name='add_job'),
    path('one_job/', views.one_job, name='one_job'),
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
    path('view_one_job/', views.view_one_job, name='view_one_job'),


    url(r'^', include('django.contrib.auth.urls')),

    ##path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('Main:password_reset_done')), name='password_reset'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name="Registration/password_reset_form.html"), name='password_reset'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Registration/password_reset_confirm.html"), name='password_reset_confirm'),
  #   url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
   #      auth_views.PasswordResetConfirmView.as_view(template_name="Registration/password_reset_confirm.html" ,success_url=reverse_lazy('users:password_reset_done')), name='password_reset_confirm'),
    #path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
