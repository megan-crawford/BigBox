from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile, Post, Review, Report, JobChoices, Review, Seeker, Creator
from . forms import ListJobsForm
from django.test import Client
from .views import sendEmail
from django.core import mail
from django.conf import settings

import os

# Create your tests here.
class DatabaseClassCreation(TestCase):
    def setUp(self):
        user = User.objects.create(username="Winky", email="winky@gmail.com", first_name="Winky", last_name="Frib")
        user.set_password("1234")
        user.save()

        Profile.objects.create(User=user, Age="23")
        post = Post.objects.create(Pay=12.50, Location="Kentucky", DateTime="2018-11-20T15:58:44.767594-06:00", Description="I love Winky", JobType="Snow Shoveling")
        Report.objects.create(Classification="No show", Details="Winky was here")
        JobChoices.objects.create(Types = "Lawn Mowing")
        review1 = Review.objects.create(Rating = 5)
        review2 = Review.objects.create(Rating = 1)
        seeker = Seeker.objects.create(User=user, Location="Delaware")
        seeker.save()
        seeker.IntJob.add(post)
        seeker.Reviews.add(review1, review2)


    def test_report(self):
        report = Report.objects.get(Details="Winky was here")
        self.assertNotEqual(report, None)
        self.assertEqual(report.Classification, "No show")
        self.assertNotEqual(report.Details, "Wrongo")

    def test_post(self):
        post = Post.objects.get(Description="I love Winky")
        self.assertNotEqual(post, None)
        self.assertEqual(post.Location, "Kentucky")
        self.assertNotEqual(post.DateTime, "Wrongo")

    def test_user(self):
        user = User.objects.get(username="Winky")
        self.assertNotEqual(user, None)
        self.assertEqual(user.last_name, "Frib")
        self.assertNotEqual(user.username, "winky")

    def test_profile(self):
        user = User.objects.get(username="Winky")
        self.assertNotEqual(user, None)
        self.assertEqual(Profile.objects.get(User=user).Age, 23)

    def test_jobchoices(self):
        choice = JobChoices.objects.get(Types = "Lawn Mowing")
        self.assertNotEqual(choice, None)

    def test_Seeker(self):
        user = User.objects.get(username="Winky")
        seeker = Seeker.objects.get(User=user)
        self.assertNotEqual(seeker, None)
        self.assertTrue(seeker.Reviews.filter(Rating = 5)[0].Rating, 5)
        self.assertTrue(seeker.Reviews.filter(Rating = 1)[0].Rating, 1)
        self.assertTrue(seeker.Reviews.filter(Rating = 2).count, 0)
    
class UpdateProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'userCopy', 'password': 'eifhieee', 'password_confirmation': 'eifhieee',
                        'email': 'email2@email.com', 'first_name': 'Jack','last_name': 'Smith', 'age': 23            
        })
        self.client.post('/create_account/', { #currently logged in as user1
                        'username': 'user1', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email@email.com', 'first_name': 'John', 'last_name': 'Smith', 'age': 20              
        })

    def test_view_valid_age(self):
        #age_button to show that the update age button was pressed
        self.client.post('/update_account/', {'age': 30, 'age_button': ''})

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.profile.Age, 30)

    def test_view_valid_email(self):
        self.client.post('/update_account/', {'email': 'new@email.com', 'email_button': ''}) 

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.email, 'new@email.com')

    def test_view_valid_all(self):
        self.client.post('/update_account/', {'password': 'oscusifwc', 'password_confirmation': 'oscusifwc', 'first_name': 'Jack', 'email': 'newer@email.com', 'age': 40, 'update_all_button': ''}) 

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.first_name, 'Jack')
        self.assertEqual(user1.email, 'newer@email.com')
        self.assertEqual(user1.profile.Age, 40)
        self.assertTrue(user1.check_password('oscusifwc'))

    def test_view_invalid_email(self):
        #email already exists
        response = self.client.post('/update_account/', {'email': 'email2@email.com', 'email_button': ''}) 
        self.assertFalse(response.context['form'].is_valid())

    def test_view_invalid_first_name(self):
        response = self.client.post('/update_account/', {'first_name': 'jack5', 'first_name_button': ''}) 
        self.assertFalse(response.context['form'].is_valid())

    def test_view_invalid_password_confirmation(self):
        response = self.client.post('/update_account/', {'password': 'aaaaaaaa', 'password_confirmation': 'bbbbbbbb', 'password_button': ''}) 
        self.assertFalse(response.context['form'].is_valid())

class CreateProfile(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_valid(self):
        self.client.post('/create_account/', {
                        'username': 'user1', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc',
                        'email': 'user@email.com', 'first_name': 'Sam', 'last_name': 'Samuel', 'age': 70
        })

        user = User.objects.filter(username='user1').first()
        self.assertNotEqual(user, None)
        self.assertTrue(Profile.objects.filter(User=user).exists())
        self.assertTrue(Seeker.objects.filter(User=user).exists())
        self.assertTrue(Creator.objects.filter(User=user).exists())

    def test_view_invalid_username(self):
        self.client.post('/create_account/', {
                        'username': 'user1', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc',
                        'email': 'email1@email.com', 'first_name': 'Sam', 'last_name': 'Samuel', 'age': 70
        })
        response = self.client.post('/create_account/', {
                                    'username': 'user1', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc',
                                    'email': 'email2@email.com', 'first_name': 'Sam', 'last_name': 'Samuel', 'age': 70
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(User.objects.filter(username='user2').exists())

    def test_view_invalid_email(self):
        response = self.client.post('/create_account/', {
                                    'username': 'user1', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc',
                                    'email': 'user@email.com', 'first_name': 'Sam', 'last_name': 'Samuel', 'age': 70
        })
        response = self.client.post('/create_account/', {
                                    'username': 'user2', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc',
                                    'email': 'user@email.com', 'first_name': 'Sam', 'last_name': 'Samuel', 'age': 70
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(User.objects.filter(username='user2').exists())

class CreateJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user', 'password': '84cn39cn93', 'password_confirmation': '84cn39cn93',
                        'email': 'jane@email.com', 'first_name': 'Jane', 'last_name': 'Keith', 'age': 16
        })

    def test_view_valid(self):
        self.client.post('/create_job/', {
                        'pay': 20.00, 'date_time': '2019-10-25',
                        'description': 'work involves ...', 'job_type': Post.BABYSITTING,
        })

        post = Post.objects.all().first() #get only object in table
        self.assertNotEqual(post, None)
        self.assertEqual(post.Pay, 20.00)

        user = User.objects.first() #get the only user
        self.assertEqual(user.creator.Posts.all().count(), 1)

    def test_view_empty_fields(self):
        response = self.client.post('/create_job/', {
                                    #no pay, no date time
                                    'description': 'work involves ...', 'job_type': Post.BABYSITTING,
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Post.objects.all().count(), 0)

    def test_view_invalid_date(self):
        response = self.client.post('/create_job/', {
                                    'pay': 20.00, 'date_time': '2000-10-25', #date was a long time ago
                                    'description': 'work involves ...', 'job_type': Post.BABYSITTING,
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Post.objects.all().count(), 0)

class GenerateReport(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user', 'password': '84cn39cn93', 'password_confirmation': '84cn39cn93',
                        'email': 'johnn@email.com', 'first_name': 'John', 'last_name': 'Doe', 'age': 18
        })

    def test_view_valid(self):
        self.client.post('/generate_report/?username=user', {
                        'classification': Report.PAYMENT, 'details': 'User did not pay payment'
        })

        report = Report.objects.first() #get only object in table
        self.assertNotEqual(report, None)
        self.assertEqual(report.Classification, Report.PAYMENT)
        self.assertEqual(report.Details, 'User did not pay payment')

        user = User.objects.first() #get the only user
        self.assertTrue(Report.objects.filter(User=user).exists())

class ListJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user1', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email@email.com', 'first_name': 'John', 'last_name': 'Smith', 'age': 20                    
        })
        self.client.post('/create_job/', {
                        'pay': 15.00, 'date_time': '2020-10-25',
                        'description': 'work involves ...', 'job_type': Post.DOGWALKING,
        })
        self.client.post('/create_job/', {
                        'pay': 20.00, 'date_time': '2021-10-25',
                        'description': 'work involves ...', 'job_type': Post.BABYSITTING,
        })
        self.client.post('/create_job/', {
                        'pay': 25.00, 'date_time': '2020-10-25',
                        'description': 'work involves ...', 'job_type': Post.DOGWALKING,
        })
        self.client.post('/create_job/', {
                        'pay': 30.00, 'date_time': '2021-10-25',
                        'description': 'work involves ...', 'job_type': Post.SNOWSHOVELING,
        })

    def test_form_valid(self):
        form = ListJobsForm({'max_distance': 100, 'job_type': Post.DOGWALKING,
                            'min_wage': 10.00, 'max_wage': 20.00,
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_wage(self):
        form = ListJobsForm({'max_distance': 100, 'job_type': Post.DOGWALKING,
                            'min_wage': 20.00, 'max_wage': 10.00, #max < min
        })
        self.assertFalse(form.is_valid())

    def test_view_correct_jobs_wage(self):
        response = self.client.post('/list_job/', {'min_wage': 15.00, 'max_wage': 25.00})
        self.assertEqual(response.context['jobs'].count(), 3)

    def test_view_correct_jobs_type(self):
        response = self.client.post('/list_job/', {'job_type': Post.DOGWALKING})
        self.assertEqual(response.context['jobs'].count(), 2)

class TestSendEmail(TestCase):
    def test1(self):
        with self.settings(
            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend',
            EMAIL_HOST = 'smtp.gmail.com',
            EMAIL_PORT = 587,
            EMAIL_HOST_USER = 'djangoBoiii@gmail.com',
            EMAIL_HOST_PASSWORD = 'Pa$Sword1',
            EMAIL_USE_TLS = True,
            DEFAULT_FROM_EMAIL = 'djangoBoiii@gmail.com'
        ):
            sendEmail("test_subject1", "test_message1", 'mkm1899@gmail.com')

    def test2(self):    
        with self.settings(
            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend',
            EMAIL_HOST = 'smtp.gmail.com',
            EMAIL_PORT = 587,
            EMAIL_HOST_USER = 'djangoBoiii@gmail.com',
            EMAIL_HOST_PASSWORD = 'Pa$Sword1',
            EMAIL_USE_TLS = True,
            DEFAULT_FROM_EMAIL = 'djangoBoiii@gmail.com'
        ):
            sendEmail("test_subject2", "test_message2", 'pattnewbie@gmail.com')
        #connection = mail.get_connection()
        #connection.open()

        #email1 = mail.EmailMessage('Hello', 'Body','djangoBoiii@gmail.com',['djangoBoiii@gmail.com'], connection=connection)
        #email1.send()
        #connection.close()
