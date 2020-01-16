from django import forms
from django.core.validators import MinLengthValidator

from .models import Sayoneuser, Story, Blog, Images,multipics
from django.core import validators
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField

class UserRegistrationform(forms.ModelForm):
    class Meta:
        model = Sayoneuser
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mailid': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'cnf_pass': forms.PasswordInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file border'}),
        }
        labels = {
            'name': 'FULLNAME',
            'mailid': 'MAIL ID',
            'username': 'USERNAME',
            'password': 'PASSWORD',
            'cnf_pass': 'CONFIRM PASSWORD',
            'profile_pic': 'PROFILE PIC'
        }


class StoryAddForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('story_user','story_author','story_likes')

        widgets = {
            'story_title':forms.TextInput(attrs={'class':'form-control'}),
            'story_type':forms.Select(attrs={'class':'form-control'}),
        }

        labels = {
            'story_title': 'Story Title',
            'story_type': 'Story Type',

        }


class AddBlog(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('story',)
        widgets = {
            'blog_pic': forms.FileInput(attrs={'class': 'form-control-file border'}),
            'blog_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'blog_pic': 'Add Image',
            'blog_description': 'Content'
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('file',)

class MultiUploadForm(forms.ModelForm):

    pics = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    class Meta:
        fields = '__all__'
        model = multipics



        labels = {
            'pics':'uploadpics',
            'text':'Desc',
        }
