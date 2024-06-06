from django.contrib import admin
from . models import *
# Register your models here.


from django.contrib.admin.views.decorators import staff_member_required


# Ensure users go through the allauth workflow when logging into admin.
admin.site.login = staff_member_required(admin.site.login, login_url='/accounts/login/')
# Run the standard admin set-up.

admin.autodiscover()
@admin.register(IPMarkRemovalRequest)
class IPMarkRemovalRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject_code', 'subject_name', 'instructor', 'dean', 'status', 'date_requested')
    # You can add more fields to list_display as needed

admin.site.register(AdditionalFile)
admin.site.register(IPMark)