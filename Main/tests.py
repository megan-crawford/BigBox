from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile

# Create your tests here.
class ATestCase(TestCase):
    def setup(self):
        
        self.testuser = User.objects.create_user(username='testuser', password='1234')
        login = self.client.login(username = 'testuser', password = '1234')
        
        #self.user.save()

    def test1(self):
        self.user = User.objects.create_user(username = 'user1', password = 'pass')
        self.profile = Profile.objects.create(User = self.user, Email = 'email@email.com',FirstName = 'First',LastName = 'Last',Description = 'Description', Age = 5)
        temp = Profile.objects.get(Email = 'email@email.com')
        self.assertEqual(temp.User, self.user)




class BTestCase(TestCase):
    def setup(self):
        self.testuser = User.objects.create_user(username='testuser', password='1234')
        login = self.client.login(username = 'testuser', password = '1234')
        
        #self.user.save()

    def test1(self):
        self.user1 = User.objects.create_user(username = 'user1', password = 'pass')
        self.user2 = User.objects.create_user(username = 'user2', password = 'pass')
        self.profile = Profile.objects.create(User = self.user1, Email = 'email@email.com',FirstName = 'First',LastName = 'Last',Description = 'Description', Age = 5)
        temp = Profile.objects.get(Email = 'email@email.com')
        self.assertNotEqual(temp.User, self.user2)


#python manage.py test Main.tests