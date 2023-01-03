from django.contrib import admin
from .models import CustomUser, Profile, Code, UserRequestIP

# Register your models here.

class UserRequestIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address','user','attempt_time','path_info','attempt_numbers')

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Code)
admin.site.register(UserRequestIP, UserRequestIPAdmin)
