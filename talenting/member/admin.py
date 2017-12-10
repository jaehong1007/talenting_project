from django.contrib import admin

from .models import GuestReview, User, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'self_intro', 'talent_intro', 'city', 'available_languages')

class GuestReviewAdmin(admin.ModelAdmin):
    list_display = ('host', 'guest', 'review', 'recommend', 'created_at')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(GuestReview, GuestReviewAdmin)
admin.site.register(Profile, ProfileAdmin)
