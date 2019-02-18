from django import forms
from django.core.exceptions import ValidationError 
from django.core.validators import EmailValidator, RegexValidator
from . models import User
from re import search #regex

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Password Confirmation', max_length=128, widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=35)
    last_name = forms.CharField(label='Last Name', max_length=35)
    location = forms.CharField(label='Location', max_length=200) #form type may need to be updated

    def save(self):
        user = User.objects.create(email=self.email, password=self.password, first_name=self.first_name, 
                                last_name=self.last_name, location=self.location)
        user.save()

    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not User.objects.filter(email=email).exists:
            raise ValidationError(message='Email already exists', code='preexisting_email')

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        
        if search('^[A-Za-z]*$', first_name) is None:
            raise ValidationError(message='First name can only contain letters', code='invalid_name')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        
        if search('^[A-Za-z]+$', last_name) is None:
            raise ValidationError(message='Last name can only contain letters', code='invalid_name')

        return last_name

    def clean_password_confirmation(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']

        if password != password_confirmation:
            raise ValidationError(message='The passwords do not match', code='invalid_password_confirmation')

        return password_confirmation