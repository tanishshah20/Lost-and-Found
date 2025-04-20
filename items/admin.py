from django.contrib import admin
from .models import LostItem, FoundItem, ItemCategory

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_lost', 'date_posted', 'is_found')
    list_filter = ('is_found', 'date_lost', 'date_posted')
    search_fields = ('title', 'description', 'location', 'user__username')

@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_found', 'date_posted', 'is_claimed')
    list_filter = ('is_claimed', 'date_found', 'date_posted')
    search_fields = ('title', 'description', 'location', 'user__username')

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)