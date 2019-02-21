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
	path('', views.home, name='home'),
	path('home/', views.home, name='home'),
    path('login/', views.login_request, name='login'),
	
	path('create_account/', views.create_account, name='create_account'),
    path('create_job/', views.create_job, name='create_job'),
    path('list_job/', views.list_job, name='list_job'),
    path('add_job/', views.new_job, name='add_job'),
    path('profile/', views.profile, name='profile'),
    path('update_account/', views.update_account, name='update_account'),
    path('true_home/', views.true_home, name='true_home'),
]
