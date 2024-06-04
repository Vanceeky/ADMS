from django.contrib import admin
from . models import *
# Register your models here.


@admin.register(IPMarkRemovalRequest)
class IPMarkRemovalRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject_code', 'subject_name', 'instructor', 'dean', 'status', 'date_requested')
    # You can add more fields to list_display as needed

admin.site.register(AdditionalFile)
admin.site.register(IPMark)