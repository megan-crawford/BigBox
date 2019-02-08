from django import forms

class RegisterForm(forms.Form):
    email = forms.CharField(max_length=254)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=35)
    last_name = forms.CharField(max_length=35)
    location = forms.CharField(max_length=200) #form type may need to be updated