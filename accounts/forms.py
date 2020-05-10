from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile


class RegisterForm(UserCreationForm):
    username=forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    email=forms.EmailField(max_length=30,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    password1=forms.CharField(max_length=30,label='Password:',widget=forms.PasswordInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    password2=forms.CharField(max_length=30,label='Password Confirmation:',widget=forms.PasswordInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    password=forms.CharField(max_length=30,widget=forms.PasswordInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    class Meta:
        fields=['username','password']


class ProfileUpdateUserForm(forms.ModelForm):
    username=forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    email=forms.EmailField(max_length=30,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    first_name=forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    last_name=forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']

class ProfileUpateMetaForm(forms.ModelForm):
    country=forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    state=forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    city=forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    about_me=forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    class Meta:
        model=Profile
        fields=['country','state','city','about_me','image']
