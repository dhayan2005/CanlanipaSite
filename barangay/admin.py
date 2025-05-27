from django.contrib import admin
from .models import ResidentProfile, Complaint, Profile

# Register your models here
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_text', 'address', 'email', 'contact_number', 'date_filed']
    list_filter = ['date_filed']
    search_fields = ('complaint_text', 'resident__username')

@admin.register(ResidentProfile)
class ResidentProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'age', 'purok', 'user')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'purok')