from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import LostItem, FoundItem, Student, ItemClaim, ItemComment

class StudentRegistrationForm(UserCreationForm):
    BRANCH_CHOICES = [
        ('CE', 'Computer Engineering'),
        ('IT', 'Information Technology'),
        ('CSDS', 'Computer Science and Engineering (Data Science)'),
        ('EXTC', 'Electronics and Telecommunication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('AIDS', 'Artificial Intelligence and Data Science'),
        ('CSIOT', 'Computer Science and Engineering (IOT and Cyber Security with Block Chain Technology)'),
    ]
    
    full_name = forms.CharField(max_length=100)
    sap_id = forms.CharField(
        max_length=11, 
        min_length=11,
        help_text='Enter your 11-digit SAP ID',
        widget=forms.TextInput(attrs={'pattern': '[0-9]{11}', 'title': 'SAP ID must be 11 digits'})
    )
    branch = forms.ChoiceField(choices=BRANCH_CHOICES)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'sap_id', 'branch', 'email', 'password1', 'password2']
    
    def clean_sap_id(self):
        sap_id = self.cleaned_data.get('sap_id')
        
        # Check if the SAP ID is numeric and 11 digits
        if not sap_id.isdigit():
            raise forms.ValidationError("SAP ID must contain only digits.")
            
        if len(sap_id) != 11:
            raise forms.ValidationError("SAP ID must be exactly 11 digits.")
            
        # Check if SAP ID is already registered
        if Student.objects.filter(sap_id=sap_id).exists():
            raise forms.ValidationError("This SAP ID is already registered.")
            
        return sap_id
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create Student profile
            Student.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                sap_id=self.cleaned_data['sap_id'],
                branch=self.cleaned_data['branch']
            )
            
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="SAP ID",
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Enter your 11-digit SAP ID'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Enter your 11-digit SAP ID"

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

class ItemClaimForm(forms.ModelForm):
    class Meta:
        model = ItemClaim
        fields = ['description', 'evidence']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please describe why you believe this item belongs to you and any identifying features...'}),
        }

class ItemCommentForm(forms.ModelForm):
    class Meta:
        model = ItemComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment or message...'}),
        }