from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile, Post, Review, Report, JobChoices, Review, Seeker, Creator
from django.test import Client

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
