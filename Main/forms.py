from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from . models import User
from re import search #regex

class CreateAccountForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=60)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Password Confirmation', max_length=128, widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    age = forms.IntegerField(label='Age', min_value=0, max_value=150)
    #location = forms.CharField(label='Location', max_length=200) #form type may need to be updated

    error_messages = {
        'passwords_not_match' : 'Passwords do not match',
        'preexisting_email' : 'Email already exists',
        'invalid_name' : 'Name can only contain letters'
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not User.objects.filter(Email=email).exists:
            raise ValidationError(message=self.error_messages['preexisting_email'], code='preexisting_email')

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        
        if search('^[A-Za-z]+$', first_name) is None:
            raise ValidationError(message=self.error_messages['invalid_name'], code='invalid_name')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        
        if search('^[A-Za-z]+$', last_name) is None:
            raise ValidationError(message=self.error_messages['invalid_name'], code='invalid_name')

        return last_name

    def clean_password_confirmation(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']

        if password != password_confirmation:
            raise ValidationError(message=self.error_messages['passwords_not_match'], code='passwords_not_match')

        return password_confirmation

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=60)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login' : 'Email or password information is incorrect',
        #by default each field is required and has error message 'This field is required.'
    }

    def clean(self):
        super().clean()

class UpdateAccountForm(CreateAccountForm):
    profile_picture = forms.ImageField(label='Update Profile Picture', required=False)
    first_name = forms.CharField(label='Update First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Update Last Name', max_length=50, required=False)
    age = forms.IntegerField(label='Update Age', min_value=0, max_value=150 , required=False)
    email = forms.EmailField(label='Update Email', max_length=60, required=False)
    description = forms.CharField(label='Update Description', required=False)
    password = forms.CharField(label='Update Password', max_length=128, required=False, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Confirm new Password', max_length=128, required=False, widget=forms.PasswordInput)