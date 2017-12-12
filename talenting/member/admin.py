from django.contrib import admin

from .models import GuestReview, User

admin.site.register(GuestReview)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name')
#     search_fields = ('email',)
#     # prepopulated_fields = {'slug': ('title',)}
#     # ordering = ['status', 'publish']

admin.site.register(User)
