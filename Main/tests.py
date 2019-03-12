from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile
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

