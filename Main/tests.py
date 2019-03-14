from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile, Post, Report
from django.test import Client

# Create your tests here.
class UpdateProfile(TestCase):
    def setUp(self):
        self.client = Client()
    
        self.user1 = User.objects.create(username='user1', email='email@email.com', first_name='John', last_name='Smith')
        self.user1.set_password('password')
        self.user1.save()
        self.profile1 = Profile.objects.create(User=self.user1, Age=20)

        isLoggedIn = self.client.login(username='user1', password='password')
        self.assertTrue(isLoggedIn)

    def test_view_valid_age(self):
        user1 = User.objects.get(username='user1')
        self.assertEqual(user1.profile.Age, 20)

        response = self.client.post('/update_account/', {'age': 20})
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
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(username='user1')
        self.assertNotEqual(user1, None)

class CreateJob(TestCase):
    def setUp(self):
        self.client = Client()

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

class CreateReport(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='user')
        self.user.set_password('password')

    def test_view_valid(self):
        response = self.client.post('/create_report/?username=user', {
                                    'classification': Report.PAYMENT,
                                    'details': 'User did not pay payment'
        })
        self.assertEqual(response.status_code, 302) #302 for redirect to profile

        report = Report.objects.all().first() #get only object in table
        self.assertNotEqual(report, None)
        self.assertEqual(report.Classification, Report.PAYMENT)
        self.assertEqual(report.Details, 'User did not pay payment')