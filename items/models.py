from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Student profile model
class Student(models.Model):
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    sap_id = models.CharField(max_length=11, unique=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)

    def __str__(self):
        return f"{self.full_name} ({self.sap_id})"

class BaseItem(models.Model):
    """Base model for both lost and found items."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
        ordering = ['-date_posted']
        
    def __str__(self):
        return self.title

class LostItem(BaseItem):
    """Model for lost items."""
    date_lost = models.DateField()
    is_found = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('lost-item-detail', kwargs={'pk': self.pk})

class FoundItem(BaseItem):
    """Model for found items."""
    date_found = models.DateField()
    is_claimed = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('found-item-detail', kwargs={'pk': self.pk})

class ItemCategory(models.Model):
    """Categories for lost and found items."""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Item Categories"

class ItemClaim(models.Model):
    """Model for item claims."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, null=True, blank=True)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(help_text="Describe why you believe this item belongs to you")
    evidence = models.FileField(upload_to='claim_evidence/', help_text="Upload any proof of ownership", null=True, blank=True)
    date_claimed = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        if self.lost_item:
            return f"Claim for lost item {self.lost_item.title} by {self.user.username}"
        else:
            return f"Claim for found item {self.found_item.title} by {self.user.username}"
    
    class Meta:
        ordering = ['-date_claimed']

class ItemComment(models.Model):
    """Model for comments on items."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_posted']
    
    def __str__(self):
        if self.lost_item:
            return f"Comment on {self.lost_item.title} by {self.user.username}"
        else:
            return f"Comment on {self.found_item.title} by {self.user.username}"