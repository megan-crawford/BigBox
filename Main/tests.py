from django.test import TestCase
from . models import Review
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')
        login = self.client.login(username='testuser', password='1234')
        Review.objects.create(Rating = 20)

    def test_user(self):
        self.client.login(email="a", password="1234")
        self.assertEqual(Review.objects.get(Rating=20).Rating, 19)
        #self.assertTrue(True)
