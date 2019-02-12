from django.db import models

# Create your models here.
class User(models.Model):
    ID = models.BigIntegerField()
    Email = models.TextField()
    Password = models.TextField()
    FirstName = models.TextField()
    Description = models.TextField()
    Age = models.SmallIntegerField()
    #image
    Contacts = models.ManyToManyField(User)
    Reports = models.ManyToManyField(Report)

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

    ID = models.BigIntegerField()
    Classification = models.CharField(
        choices=REPORT_CHOICES
    )
    Details = models.TextField()

class Seeker(User):     #Job Seeker, subclass to User
    
    PrefType = models.ManyToManyField(Post.TYPE_CHOICES)
    IntJob = models.ManyToManyField(Post)
    Reviews = models.ManyToManyField(Review)
    Location = models.TextField()

class Creator(User):    #Job Creator
    Posts = models.ManyToManyField(Post)
    Reviews = models.ManyToManyField(Review)

class Review(models.Model):
    ID = models.BigIntegerField()
    Rating = models.SmallIntegerField() #Precision undecided

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

    ID = models.BigIntegerField()
    Pay = models.FloatField()
    Location = models.TextField()
    DateTime = models.DateTimeField()
    Interested = models.ManyToManyField(Seeker)
    Description = models.TextField()
    JobType = models.ManyToManyField(TYPE_CHOICES)    
