from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class ATestCase(TestCase):
    def setup(self):
        self.user = User.objects.create_user('user1', 'email@email.com', 'pass')
        self.user.save()

    def test1(self):
        self.assertTrue(True)
        