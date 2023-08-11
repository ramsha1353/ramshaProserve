from django.contrib import admin
from proserve_app.models import UserProfile, WorkerProfile, ClientProfile

# Register your models here.
@admin.register(UserProfile)
class registerAdmin(admin.ModelAdmin):
    list_display = ['Address', 'phone_no','experiance','gender','user_type']
@admin.register(WorkerProfile)
class WorkerAdmin(admin.ModelAdmin):
    list_display = [ 'profile', 'service', 'description', 'price_per_day', 'available_time' ]

@admin.register(ClientProfile)
class ClientAdmin(admin.ModelAdmin):
    list_display = [ 'profile']

