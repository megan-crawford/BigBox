from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile, Post, Report
from django.test import Client

# Create your tests here.
class UpdateProfile(TestCase):
    def setUp(self):
        self.client = Client()
    
        self.client.post('/create_account/', {
                                    'username': 'user1',
                                    'password': 'vf83g9f7fg',
                                    'password_confirmation': 'vf83g9f7fg',
                                    'email': 'email@email.com',
                                    'first_name': 'John',
                                    'last_name': 'Smith',
                                    'age': 20              
        })

    def test_view_valid_age(self):
        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.profile.Age, 20)

        #age_button to show that the update age button was pressed
        response = self.client.post('/update_account/', {'age': 30, 'age_button': ''}) 
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.profile.Age, 30)

class CreateProfile(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view(self):
        response = self.client.post('/create_account/', {
                                    'username': 'user1',
                                    'password': 'vf83g9f7fg',
                                    'password_confirmation': 'vf83g9f7fg',
                                    'email': 'email@email.com',
                                    'first_name': 'John',
                                    'last_name': 'Smith',
                                    'age': 20
                                
        })
        self.assertEqual(response.status_code, 302) #redirect to home


        user1 = User.objects.get(username='user1')
        self.assertNotEqual(user1, None)

class CreateJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user1',
                        'password': 'vf83g9f7fg',
                        'password_confirmation': 'vf83g9f7fg',
                        'email': 'email@email.com',
                        'first_name': 'John',
                        'last_name': 'Smith',
                        'age': 20                    
        })

    def test_view_valid(self):
        response = self.client.post('/create_job/', {
                                    'pay': 20.00,
                                    'date_time': '2019-10-25',
                                    'description': 'work involves ...',
                                    'job_type': Post.BABYSITTING,
        })
        self.assertEqual(response.status_code, 302) #302 for redirect to add job

        post = Post.objects.all().first() #get only object in table
        self.assertNotEqual(post, None)
        self.assertEqual(post.Pay, 20.00)

        user = User.objects.first() #get the only user
        self.assertEqual(user.creator.Posts.all().count(), 1)

    def test_view_empty_fields(self):
        response = self.client.post('/create_job/', {
                                    #no pay
                                    #no date time
                                    'description': 'work involves ...',
                                    'job_type': Post.BABYSITTING,
        })
        self.assertEqual(response.status_code, 200) #200 for redirect to create job
        self.assertEqual(Post.objects.all().count(), 0)

    def test_view_invalid_date(self):
        response = self.client.post('/create_job/', {
                                    'pay': 20.00,
                                    'date_time': '2000-10-25', #date was a long time ago
                                    'description': 'work involves ...',
                                    'job_type': Post.BABYSITTING,
        })
        self.assertEqual(response.status_code, 200) #200 for redirect to create job
        self.assertEqual(Post.objects.all().count(), 0)

class GenerateReport(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='user')

    def test_view_valid(self):
        response = self.client.post('/generate_report/?username=user', {
                                    'classification': Report.PAYMENT,
                                    'details': 'User did not pay payment'
        })
        self.assertEqual(response.status_code, 302) #302 for redirect to profile page

        report = Report.objects.first() #get only object in table
        self.assertNotEqual(report, None)
        self.assertEqual(report.Classification, Report.PAYMENT)
        self.assertEqual(report.Details, 'User did not pay payment')

class ListJob(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/create_account/', {
                        'username': 'user1',
                        'password': 'vf83g9f7fg',
                        'password_confirmation': 'vf83g9f7fg',
                        'email': 'email@email.com',
                        'first_name': 'John',
                        'last_name': 'Smith',
                        'age': 20                    
        })
        self.client.post('/create_job/', {
                        'pay': 15.00,
                        'date_time': '2020-10-25',
                        'description': 'work involves ...',
                        'job_type': Post.DOGWALKING,
        })

    def test_view_valid(self):
        response = self.client.get('/list_job/', {
                                    'max_distance': 100,
                                    'job_type': Post.DOGWALKING,
                                    'min_wage': 10.00,
                                    'max_wage': 20.00,
        })
        self.assertEqual(response.context['jobs'].all().count(), 1)
        self.assertEqual(response.context['jobs'].first().Pay, 15.00)

    def test_view_invalid_wage(self):
        response = self.client.get('/list_job/', {
                                    'max_distance': 100,
                                    'job_type': Post.DOGWALKING,
                                    'min_wage': 20.00,
                                    'max_wage': 10.00,
        })
        self.assertFalse(response.context['form'].is_valid())

