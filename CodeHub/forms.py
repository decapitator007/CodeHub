from django import forms
from .models import Question,Answer
class signin(forms.Form):
    username=forms.CharField(label='Username')
    password=forms.CharField(label='Password',widget=forms.PasswordInput())
class signup(forms.Form):
    firstname=forms.CharField(label='First Name')
    lastname=forms.CharField(label='Last Name')
    username=forms.CharField(label='Username')
    email=forms.EmailField(label='Email')
    cf=forms.CharField(label='Codeforces ID (Optional)',required=False)
    password=forms.CharField(label='Password (Length of the password must be from 8-16)',widget=forms.PasswordInput())
    cpassword=forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
class QForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=('content',)
        labels={'content':''}
class AForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=('content',)
        labels={'content':''}
