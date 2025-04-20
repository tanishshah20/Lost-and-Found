from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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