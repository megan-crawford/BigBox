from django.db import models
from django.conf import settings

# Create your models here.

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

    Pay = models.FloatField()
    Location = models.TextField()
    DateTime = models.DateTimeField()
    #Interested = models.ManyToManyField(Seeker)
    Description = models.TextField()
    JobType = models.CharField(
            max_length=100,
            choices=TYPE_CHOICES,
    )

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

class User(models.Model):
    User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    Email = models.TextField()
    Password = models.TextField()
    FirstName = models.TextField()
    Description = models.TextField()
    Age = models.SmallIntegerField()
    #image
    Contacts = models.ManyToManyField("self", blank=True)
    Reports = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)

class JobChoices(models.Model):
    Types = models.CharField(
            max_length=100,
            choices=Post.TYPE_CHOICES,
    )
            
class Review(models.Model):
    Rating = models.SmallIntegerField() #Precision undecided

class Seeker(User):     #Job Seeker, subclass to User
    
    PrefType = models.ForeignKey(
            JobChoices,
            on_delete=models.CASCADE,
    )
    IntJob = models.ManyToManyField(Post)
    Reviews = models.ManyToManyField(Review)
    Location = models.TextField()

class Creator(User):    #Job Creator
    Posts = models.ManyToManyField(Post)
    Reviews = models.ManyToManyField(Review)


