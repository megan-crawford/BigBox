from django.contrib.auth.models import User
from enum import Enum
from django.db import models
import os
import pandas

locations = pandas.read_csv('zip_code_database.csv', index_col=['zip'], usecols=['zip', 'state', 'latitude', 'longitude'])

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class Post(models.Model):
    LAWNMOWING='LM'
    SNOWSHOVELING='SS'
    DOGWALKING='DW'
    PETSITTING='PS'
    BABYSITTING='BS'
    CLEANING='C'
    MOVING='M'
    OTHER='O'

    TYPE_CHOICES = (
            (LAWNMOWING, 'Lawn Mowing'),
            (SNOWSHOVELING, 'Snow Shoveling'),
            (DOGWALKING, 'Dog Walking'),
            (PETSITTING, 'Pet Sitting'),
            (BABYSITTING, 'Baby Sitting'),
            (CLEANING, 'Cleaning'),
            (MOVING, 'Moving'),
            (OTHER, 'Other'),
    )

    ACTIVE_CHOICES = (
            (0, 'OPEN'),
            (1, 'CLOSED'),
            (2, 'CHOSEN'),
    )

    userID = models.IntegerField(default=0)
    userName = models.CharField(max_length=100, default="default")
    Pay = models.FloatField()
    ZipCode = models.IntegerField()
    DateTime = models.DateTimeField()
    Interested = models.ManyToManyField(User, related_name='interested_seekers', blank=True)
    Description = models.TextField()
    JobType = models.CharField(
            max_length=100,
            choices=TYPE_CHOICES,
    )
    Active = models.SmallIntegerField(
            choices=ACTIVE_CHOICES,
            default=0,
    )

    Chosen = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #posts=models.Manager()

class Report(models.Model):
    PAYMENT = 'PI'
    VIOLENCE = 'V'
    NOSHOW = 'NS'
    SCAM = 'S'
    OTHER = 'O'

    REPORT_CHOICES = (    
        (PAYMENT, 'Payment Issue'),
        (VIOLENCE, 'Violence'),
        (NOSHOW, 'No show'),
        (SCAM, 'Scam'),
        (OTHER, 'Other'),
    )

    Classification = models.CharField(
        max_length=100,
        choices=REPORT_CHOICES
    )
    Details = models.TextField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    #Email = models.CharField(max_length = 60)
    #FirstName = models.CharField(max_length = 50)
    #LastName = models.CharField(max_length = 50)
    Description = models.TextField()
    Age = models.SmallIntegerField()
    Portrait = models.ImageField(upload_to='Main/static/images/profile_pictures/', blank=True, null=True)
    Contacts = models.ManyToManyField("self", blank=True)
    ZipCode = models.IntegerField(blank=True, null=True)
    isNotified = models.BooleanField(default=False)

    #Token = models.CharField(max_length=80, blank=True, null=True)
    isVerified = models.BooleanField(default=False)
            
class SeekerReview(models.Model):
    Rating = models.SmallIntegerField() #Precision undecided
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seeker_reviews')

class CreatorReview(models.Model):
    Rating = models.SmallIntegerField() #Precision undecided
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_reviews')

class Seeker(models.Model):     #Job Seeker, subclass to User
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    PrefType = models.CharField(max_length=2, choices=Post.TYPE_CHOICES, blank=True, null=True)
    IntJob = models.ManyToManyField(Post, blank=True)
    Location = models.TextField(blank=True, null=True)

    def get_pref_job_type(self):
        if self.PrefType:
            return dict(Post.TYPE_CHOICES)[self.PrefType]
        else:
            return None

class Creator(models.Model):    #Job Creator
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Posts = models.ManyToManyField(Post, blank=True)
