from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class UserAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None): #try out email for param name
        print('auth function')
        try:
            user = User.objects.get(email=username) #replace username with email
        except User.DoesNotExist:
            print('auth user does not exist')
            return None
        
        if user.check_password(password):
                return user
        else:
            print('auth password is not right')
            return None
