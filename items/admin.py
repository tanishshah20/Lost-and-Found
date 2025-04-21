from django.contrib import admin
from .models import LostItem, FoundItem, ItemCategory, Student, ItemClaim, ItemComment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'sap_id', 'branch', 'user')
    search_fields = ('full_name', 'sap_id', 'user__username')
    list_filter = ('branch',)

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

@admin.register(ItemClaim)
class ItemClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_title', 'date_claimed', 'is_approved')
    list_filter = ('is_approved', 'date_claimed')
    search_fields = ('user__username', 'description')
    
    def get_item_title(self, obj):
        if obj.lost_item:
            return f"Lost: {obj.lost_item.title}"
        elif obj.found_item:
            return f"Found: {obj.found_item.title}"
        return "No item"
    get_item_title.short_description = 'Item'

@admin.register(ItemComment)
class ItemCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_title', 'get_content_preview', 'date_posted')
    list_filter = ('date_posted',)
    search_fields = ('user__username', 'content')
    
    def get_item_title(self, obj):
        if obj.lost_item:
            return f"Lost: {obj.lost_item.title}"
        elif obj.found_item:
            return f"Found: {obj.found_item.title}"
        return "No item"
    get_item_title.short_description = 'Item'
    
    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = 'Content'