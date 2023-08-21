from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from proserve_app.models import UserProfile, WorkerProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Prevents users from deleting the user profile when editing the User

# Register the inline admin class
UserAdmin.inlines = (UserProfileInline,)

# Re-register the UserAdmin class
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

# Unregister the default UserAdmin and register your custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Register your models here.
# @admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user',  'phone_no','user_type']
admin.site.register(UserProfile, UserProfileAdmin)





@admin.register(WorkerProfile)
class WorkerAdmin(admin.ModelAdmin):
    list_display = [ 'profile', 'service', 'description', 'price_per_day','experiance', 'available_time' ]


