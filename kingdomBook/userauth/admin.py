from django.contrib import admin
from userauth.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username',]
    
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['full_name', 'bio', 'phone']


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
