from django import forms
from .models import LostItem, FoundItem, ItemCategory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'location', 'date_lost', 'image']
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date'}),
        }

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['title', 'description', 'location', 'date_found', 'image']
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']