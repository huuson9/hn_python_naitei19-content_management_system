from django import forms
from django.contrib.auth.forms import UserCreationForm

from . models import User, Comment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        context = {
            'first_name': forms.TextInput(attrs={'class': 'first-name-control'}),
            'last_name': forms.TextInput(attrs={'class': 'last-name-control'}),  
            'email': forms.EmailInput(attrs={'class': 'email-control'}),
            'username': forms.TextInput(attrs={'class': 'username-control'}),
        }

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': ''
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here', 'id': 'comment_text'}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 
