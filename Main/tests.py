from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile, Post, Report, SeekerReview, CreatorReview, Seeker, Creator
from . forms import ListJobsForm, GenerateReportForm, CreateJobForm
from django.test import Client
from .views import sendEmail, distBetween
from django.core import mail
from django.conf import settings
from django.db.models.fields import BLANK_CHOICE_DASH
from base64 import b64encode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

import re
import os

# Create your tests here.
class DatabaseClassCreation(TestCase):
    def setUp(self):
        user = User.objects.create(username="Winky", email="winky@gmail.com", first_name="Winky", last_name="Frib")
        user.set_password("1234")
        user.save()

        Profile.objects.create(User=user, Age="23")
        post = Post.objects.create(Pay=12.50, ZipCode=12345, DateTime="2018-11-20T15:58:44.767594-06:00", Description="I love Winky", JobType="Snow Shoveling")
        Report.objects.create(User=user, Classification="No show", Details="Winky was here")
        review1 = SeekerReview.objects.create(Rating = 5, User = user)
        review2 = CreatorReview.objects.create(Rating = 1, User = user)
        seeker = Seeker.objects.create(User=user, Location="Delaware")
        seeker.save()
        seeker.IntJob.add(post)
        user.seeker_reviews.add(review1)
        user.creator_reviews.add(review2)


    def test_report(self):
        report = Report.objects.get(Details="Winky was here")
        self.assertNotEqual(report, None)
        self.assertEqual(report.Classification, "No show")
        self.assertNotEqual(report.Details, "Wrongo")

    def test_post(self):
        post = Post.objects.get(Description="I love Winky")
        self.assertNotEqual(post, None)
        self.assertEqual(post.ZipCode, 12345)
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

    def test_Seeker(self):
        user = User.objects.get(username="Winky")
        seeker = Seeker.objects.get(User=user)
        self.assertNotEqual(seeker, None)
        self.assertTrue(user.seeker_reviews.filter(Rating = 5)[0].Rating, 5)
        self.assertTrue(user.creator_reviews.filter(Rating = 1)[0].Rating, 1)
        self.assertTrue(user.seeker_reviews.filter(Rating = 2).count, 0)
    
class UpdateProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'userCopy', 'password': 'eifhieee', 'password_confirmation': 'eifhieee',
                        'email': 'email2@email.com', 'first_name': 'Jack','last_name': 'Smith', 'age': 23            
        })
        self.client.post('/create_account/', { #currently logged in as user1
            'username': 'user1', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg', 'zip_code': '12345',
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

    def test_view_valid_pref_type(self):
        self.client.post('/update_account/', {'pref_job_type': Post.BABYSITTING, 'pref_job_type_button': ''}) 

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.seeker.PrefType, Post.BABYSITTING)

    def test_view_valid_pref_job_type(self):
        self.client.post('/update_account/', {'pref_job_type': Post.BABYSITTING, 'pref_job_type_button': ''}) 

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.seeker.PrefType, Post.BABYSITTING)

    def test_view_valid_all(self):
        self.client.post('/update_account/', {'password': 'oscusifwc', 'password_confirmation': 'oscusifwc', 'zip_code': '12345',
                        'first_name': 'Jack', 'email': 'newer@email.com', 'age': 40, 'update_all_button': ''}) 

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.first_name, 'Jack')
        self.assertEqual(user1.email, 'newer@email.com')
        self.assertEqual(user1.profile.Age, 40)
        self.assertTrue(user1.check_password('oscusifwc'))
        self.assertEqual(user1.seeker.PrefType, None)

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
            'username': 'user1', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc', 'zip_code': '12345',
                        'email': 'user@email.com', 'first_name': 'Sam', 'last_name': 'Samuel', 'age': 70
        })

        user = User.objects.filter(username='user1').first()
        self.assertNotEqual(user, None)
        self.assertTrue(Profile.objects.filter(User=user).exists())
        self.assertTrue(Seeker.objects.filter(User=user).exists())
        self.assertTrue(Creator.objects.filter(User=user).exists())

    def test_view_invalid_username(self):
        self.client.post('/create_account/', {
            'username': 'user1', 'password': '83bc7493bc', 'password_confirmation': '83bc7493bc', 'zip_code': '12345', 
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

    def test_view_verified_email(self):
        self.client.post('/create_account/', {
                        'username': 'user', 'password': '83nc0924nc20', 'password_confirmation': '83nc0924nc20',
                        'email': 'user@school.edu', 'first_name': 'Sam', 'last_name': 'Jackson', 'age': 42
        })

        user = User.objects.get(username='user')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = account_activation_token.make_token(user)
        self.client.get(f'/activate/{uid}/{token}/')

        user = User.objects.get(username='user')
        self.assertEqual(user.profile.isVerified, True)

class CreateJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
            'username': 'user', 'password': '84cn39cn93', 'password_confirmation': '84cn39cn93', 'zip_code': '12345',
                        'email': 'jane@email.com', 'first_name': 'Jane', 'last_name': 'Keith', 'age': 16
        })

    def test_view_valid(self):
        self.client.post('/create_job/', {
                        'pay': 10.00, 'date_time': '2019-10-25', 'zip_code': '99811',
                        'description': 'work involves ...', 'job_type': Post.BABYSITTING,
        })

        post = Post.objects.all().first() #get only object in table
        self.assertNotEqual(post, None)
        self.assertEqual(post.Pay, 10.00)

        user = User.objects.first() #get the only user
        self.assertEqual(user.creator.Posts.all().count(), 1)

    def test_view_empty_fields(self):
        response = self.client.post('/create_job/', {
                                    'pay': None, 'date_time': '', 'zip_code': '99811',
                                    'description': 'will be moving ...', 'job_type': Post.MOVING,
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Post.objects.all().count(), 0)

    def test_view_invalid_date(self):
        response = self.client.post('/create_job/', {
                                    'pay': 20.00, 'date_time': '2000-10-25', #date was a long time ago, 
                                    'description': 'work is ...', 'job_type': Post.SNOWSHOVELING, 'zip_code': '99811',
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Post.objects.all().count(), 0)

    def test_view_invalid_pay(self):
        response = self.client.post('/create_job/', {
                                    'pay': -20.00, 'date_time': '2020-10-25', 'zip_code': '99811',
                                    'description': 'work will be ...', 'job_type': Post.DOGWALKING,
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Post.objects.all().count(), 0)

    def test_form_valid_zip_code(self):
        form = CreateJobForm({'pay': 20.00, 'date_time': '2020-10-25', 'zip_code': '99811',
                                'description': 'work will be ...', 'job_type': Post.DOGWALKING})
        self.assertTrue(form.is_valid())

    def test_form_invalid_zip_code(self):
        form = CreateJobForm({'pay': 20.00, 'date_time': '2020-10-25', 'zip_code': '99813',
                                    'description': 'work will be ...', 'job_type': Post.DOGWALKING})
        self.assertFalse(form.is_valid())

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

    def test_form_invalid_empty_details(self):
        form = GenerateReportForm({'classification': Report.PAYMENT, 'details': ''})
        self.assertFalse(form.is_valid())

class ListJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', { #user requered to be logged in to create jobs
                        'username': 'user1', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email@email.com', 'first_name': 'John', 'last_name': 'Smith', 'age': 20                    
        }) 
        self.user1 = User.objects.all().first() #get only user

        self.client.post('/create_job/', {
                        'pay': 15.00, 'date_time': '2020-10-25', 'zip_code': 94803, #far
                        'description': 'job1', 'job_type': Post.DOGWALKING,
        })
        self.client.post('/create_job/', {
                        'pay': 20.00, 'date_time': '2021-10-25', 'zip_code': 99811, #far
                        'description': 'job2', 'job_type': Post.BABYSITTING,
        })
        self.client.post('/create_job/', {
                        'pay': 25.00, 'date_time': '2020-10-25', 'zip_code': 52404, #close
                        'description': 'job3', 'job_type': Post.SNOWSHOVELING,
        })
        self.client.post('/create_job/', {
                        'pay': 30.00, 'date_time': '2021-10-25', 'zip_code': 52403, #closest
                        'description': 'job4', 'job_type': Post.DOGWALKING,
        })
        #Post.objects.create(Pay=998, DateTime="2000-10-10", Description="job5", JobType="Snow Shoveling", ZipCode=12345, userID=self.user1.id, userName=self.user1.username)

        self.client.post('/create_account/', {
                        'username': 'user2', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email2@email.com', 'first_name': 'John', 'last_name': 'Jackson', 'age': 30                  
        })
        self.client.post('/update_account/', {'zip_code': 52403, 'zip_code_button': ''})
        self.client.post('/update_account/', {'pref_job_type': Post.SNOWSHOVELING, 'pref_job_type_button': ''})
       
        #print(Post.objects.filter(Description='job5'))        

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
        response = self.client.get('/list_job/', {'min_wage': 15.00, 'max_wage': 25.00})
        self.assertEqual(len(response.context['jobs']), 3)

    # def test_view_correct_jobs_status_closed(self):
    #     response = self.client.get('/list_job/', {'min_wage': 500.00}) #get job5
    #     self.assertEqual(response.context['jobs'][0].Active, 1)

    def test_view_correct_jobs_max_wage(self):
        response = self.client.get('/list_job/', {'max_wage': 20.00})
        self.assertEqual(len(response.context['jobs']), 2)

    def test_view_correct_jobs_min_wage(self):
        response = self.client.get('/list_job/', {'min_wage': 20.00})
        self.assertEqual(len(response.context['jobs']), 3)

    def test_view_correct_jobs_type(self):
        response = self.client.get('/list_job/', {'job_type': Post.DOGWALKING})
        self.assertEqual(len(response.context['jobs']), 2)

    def test_view_correct_jobs_type_and_wage(self):
        response = self.client.get('/list_job/', {'job_type': Post.DOGWALKING, 'min_wage': 15.00, 'max_wage': 25.00})
        self.assertEqual(len(response.context['jobs']), 1)

    def test_view_sort_by_zip_code(self):
        response = self.client.get('/list_job/', {'job_type': BLANK_CHOICE_DASH})
        self.assertEqual(response.context['jobs'][0].Description, 'job4')
        self.assertEqual(response.context['jobs'][1].Description, 'job3')

    def test_view_recommended(self):
        response = self.client.get('/list_job/', {'job_type': 'FF'}) #(FF, Recommended)
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0].JobType, Post.SNOWSHOVELING)

    def test_view_search(self):
        response = self.client.get('/list_job/', {'search': 'job4'})
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0].Description, 'job4')

class AllJobsCreator(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', { #user requered to be logged in to create jobs
                        'username': 'user', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email3@email.com', 'first_name': 'Jack', 'last_name': 'Smith', 'age': 24                   
        })
        self.client.post('/create_job/', {
                        'pay': 4.00, 'date_time': '2020-5-20', 'zip_code': 12345,
                        'description': 'work involves ...', 'job_type': Post.DOGWALKING,
        })
        self.client.post('/create_job/', {
                        'pay': 50.00, 'date_time': '2021-10-13', 'zip_code': 12345,
                        'description': 'work involves ...', 'job_type': Post.BABYSITTING,
        })
        self.client.post('/create_job/', {
                        'pay': 13.00, 'date_time': '2020-10-26', 'zip_code': 12345,
                        'description': 'work involves ...', 'job_type': Post.SNOWSHOVELING,
        })

    def test_view_correct_jobs_max_wage(self):
        response = self.client.get('/all_jobs_creator/all_jobs/', {'max_wage': 13.00})
        self.assertEqual(response.context['jobs'].count(), 2)

    def test_view_correct_jobs_min_wage(self):
        response = self.client.get('/all_jobs_creator/all_jobs/', {'min_wage': 30.00})
        self.assertEqual(response.context['jobs'].count(), 1)

    def test_view_correct_jobs_wage(self):
        response = self.client.get('/all_jobs_creator/all_jobs/', {'min_wage': 4.00, 'max_wage': 25.00})
        self.assertEqual(response.context['jobs'].count(), 2)

    def test_view_correct_jobs_type(self):
        response = self.client.get('/all_jobs_creator/all_jobs/', {'job_type': Post.DOGWALKING})
        self.assertEqual(response.context['jobs'].count(), 1)

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

    def test3(self):
        email = input("Enter your email: ")
        with self.settings(
            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend',
            EMAIL_HOST = 'smtp.gmail.com',
            EMAIL_PORT = 587,
            EMAIL_HOST_USER = 'djangoBoiii@gmail.com',
            EMAIL_HOST_PASSWORD = 'Pa$Sword1',
            EMAIL_USE_TLS = True,
            DEFAULT_FROM_EMAIL = 'djangoBoiii@gmail.com'
        ):
            sendEmail("test_subject3", "test_message3", email)

    def test4(self):
        subject = input("Enter the subject: ")
        message = input("Enter the message: ")
        email = input("Enter your email: ")
        with self.settings(
            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend',
            EMAIL_HOST = 'smtp.gmail.com',
            EMAIL_PORT = 587,
            EMAIL_HOST_USER = 'djangoBoiii@gmail.com',
            EMAIL_HOST_PASSWORD = 'Pa$Sword1',
            EMAIL_USE_TLS = True,
            DEFAULT_FROM_EMAIL = 'djangoBoiii@gmail.com'
        ):
            num = sendEmail(subject, message, email)
            print(num)
        #connection = mail.get_connection()
        #connection.open()

        #email1 = mail.EmailMessage('Hello', 'Body','djangoBoiii@gmail.com',['djangoBoiii@gmail.com'], connection=connection)
        #email1.send()
        #connection.close()

class ReopenJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', { #user requered to be logged in to create jobs
                        'username': 'user', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email@email.com', 'first_name': 'John', 'last_name': 'Smith', 'age': 24                   
        })
        self.client.post('/create_job/', {
                        'pay': 45.00, 'date_time': '2020-09-25', 'zip_code': '12345',
                        'description': 'work involves ...', 'job_type': Post.DOGWALKING,
        })

        self.client.post('/create_account/', {
                        'username': 'user2', 'password': 'vf83g9f7fg', 'password_confirmation': 'vf83g9f7fg',
                        'email': 'email2@email.com', 'first_name': 'John', 'last_name': 'Jackson', 'age': 30                  
        })

        #TODO: add more actions for having a seeker accept the job and closing the job

    def test_view(self):
        post = self.client.get('/list_job/', {'min_wage': 15.00, 'max_wage': 50.00})
        postid = post.context['jobs'][0].id
        self.client.post("/reopen_job/%d"%(postid))
        post = Post.objects.first()
        self.assertEqual(post.Active, 0)

class ZipCodeDist(TestCase):
    def test_valid(self):
        realDist = 2399.4 #according to google maps
        approxDist = distBetween(99811, 48380)
        self.assertTrue(abs(realDist - approxDist) <= 1)

    def test_invalid(self):
        self.assertEqual(distBetween(99811, 48384), -1)

class GenerateReview(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', { #user1 is being reviewed
                        'username': 'user', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'jack@email.com', 'first_name': 'John', 'last_name': 'Doe', 'age': 27
        })
        self.client.post('/create_account/', { #user2 does the reviewing
                        'username': 'user2', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'jack2@email.com', 'first_name': 'John', 'last_name': 'Doe', 'age': 37
        })
        self.user = User.objects.get(username="user")

    def test_view_valid_seeker(self):
        self.client.post(f'/generate_review/{self.user.id}/1/', {'rating': 5})
        
        self.assertEqual(SeekerReview.objects.count(), 1)
        self.assertEqual(CreatorReview.objects.count(), 0)
        
        rating = self.user.seeker_reviews.first().Rating
        self.assertEqual(rating, 5)

    def test_view_valid_creator(self):
        self.client.post(f'/generate_review/{self.user.id}/0/', {'rating': 3})
        
        self.assertEqual(SeekerReview.objects.count(), 0)
        self.assertEqual(CreatorReview.objects.count(), 1)

        rating = self.user.creator_reviews.first().Rating
        self.assertEqual(rating, 3)

    def test_profile_seeker(self):
        self.client.post(f'/generate_review/{self.user.id}/1/', {'rating': 5})
        self.client.post(f'/generate_review/{self.user.id}/1/', {'rating': 4})
        self.client.post(f'/generate_review/{self.user.id}/1/', {'rating': 5})

        response = self.client.get(f'/profile/?username={self.user.username}')
        self.assertAlmostEqual(response.context['seekerScore'], 4.6667, places=4)
        self.assertEqual(response.context['creatorScore'], -1)

    def test_profile_creator(self):
        self.client.post(f'/generate_review/{self.user.id}/0/', {'rating': 3})
        self.client.post(f'/generate_review/{self.user.id}/0/', {'rating': 5})
        self.client.post(f'/generate_review/{self.user.id}/0/', {'rating': 2})

        response = self.client.get(f'/profile/?username={self.user.username}')
        self.assertAlmostEqual(response.context['creatorScore'], 3.3333, places=4)
        self.assertEqual(response.context['seekerScore'], -1)

class OneJobCreator(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'jack@email.com', 'first_name': 'John', 'last_name': 'Doe', 'age': 27
        })
        self.client.post('/create_account/', {
                        'username': 'user2', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'jack2@email.com', 'first_name': 'Jackson', 'last_name': 'Doe', 'age': 37
        })
        self.client.post('/create_account/', { #logged in as user3
                        'username': 'user3', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'jack3@email.com', 'first_name': 'Jack', 'last_name': 'Doe', 'age': 47
        })
        self.user1 = User.objects.get(username="user")
        self.user2 = User.objects.get(username="user2")
        self.user3 = User.objects.get(username="user3")

        self.client.post('/create_job/', {
                        'pay': 10.00, 'date_time': '2020-05-25', 'zip_code': 44328,
                        'description': 'work involves ...', 'job_type': Post.PETSITTING,
        })
        self.post = Post.objects.first()
        self.post.Interested.add(self.user1)
        self.post.Interested.add(self.user2)

    def test_view_valid(self):
        response = self.client.post(f'/one_job_creator/{self.post.id}/')
        self.assertEqual(response.context['interested_seekers'].count(), 2)

class InterestedSeeker(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user1', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'user1@email.com', 'first_name': 'Jackson', 'last_name': 'Doe', 'age': 28
        })
        self.user1 = User.objects.filter(username='user1').first()

        self.client.post('/create_job/', { #user1 creates job
                        'pay': 13.00, 'date_time': '2020-10-26', 'zip_code': 12345,
                        'description': 'job', 'job_type': Post.BABYSITTING,
        })
        self.job = Post.objects.filter(Description='job').first()

        self.client.post('/create_account/', {
                        'username': 'user2', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'user2@email.com', 'first_name': 'Jackson', 'last_name': 'Doe', 'age': 28
        })
        self.user2 = User.objects.filter(username='user2').first()

        self.client.post(f'/show_interest/{self.job.id}/{self.user2.id}/') #user2 shows interest in user1's job

        self.client.post('/login/', {'username': 'user1', 'password': '83c9bqo87n'})

    def test_accept(self):
        self.client.post(f'/hire_seeker/{self.job.id}/{self.user2.id}/{self.user1.id}') #user1 hires user2
        self.job = Post.objects.filter(Description='job').first() #update job
        self.assertEquals(self.job.Active, 2) #job is chosen
        self.assertEquals(self.job.Chosen.id, self.user2.id)

    def test_ignore(self):
        self.job = Post.objects.filter(Description='job').first() #update job
        self.assertEquals(self.job.Active, 0) #job is open
        self.assertEquals(self.job.Chosen, None)

class DeleteJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'user@email.com', 'first_name': 'Jackson', 'last_name': 'Smith', 'age': 16
        })

        self.client.post('/create_job/', { #user1 creates job1
                        'pay': 20.00, 'date_time': '2021-10-26', 'zip_code': 12345,
                        'description': 'job1', 'job_type': Post.CLEANING,
        })
        self.client.post('/create_job/', { #user1 creates job2
                        'pay': 30.00, 'date_time': '2020-10-26', 'zip_code': 12345,
                        'description': 'job2', 'job_type': Post.DOGWALKING,
        })
        self.job1 = Post.objects.get(Description='job1')
        self.job2 = Post.objects.get(Description='job2')
    
    def test_correct(self):
        self.assertEqual(Post.objects.count(), 2)
        self.client.get(f'/delete_job/{self.job1.id}/')
        self.assertEqual(Post.objects.count(), 1)
        response = self.client.post('/all_jobs_creator/all_jobs/')
        self.assertEqual(response.context['jobs'][0].id, self.job2.id)

def ResetPassword(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user', 'password': '83c9bqo87n', 'password_confirmation': '83c9bqo87n',
                        'email': 'user@email.com', 'first_name': 'John', 'last_name': 'Smith', 'age': 43
        })
