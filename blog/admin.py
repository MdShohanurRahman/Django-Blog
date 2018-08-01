from django.contrib import admin
from .models import *


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['author', 'title']
    list_editable = ['status']
    date_hierarchy = ('created')
    prepopulated_fields = {'slug': ('title',)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'photo']


admin.site.register(profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(comment)
