from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'base'
urlpatterns = [

    #Student URLS
    path('student-dashboard/', views.dashboard, name='student-dashboard'),
    path('request/pending/', views.request_page, name='request-page'),
    path('request/process/', views.request_process_page, name='request-process-page'),
    path('request/approved/', views.request_approved_page, name='request-approved-page'),

    path('requestIPMarkRemoval/', views.requestIPMarkRemoval, name='requestIPMarkRemoval'),

    #Faculty URLS
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty-dashboard'),
    path('submit-IP-Mark/', views.submitIPMark, name='submit-IP-Mark'),


    #BASE urls
    path('instructors-autocomplete/', views.instructors_autocomplete, name='instructors-autocomplete'),


    #DEAN URLS
    path('dean-dashboard/', views.dean_dashboard, name='dean-dashboard'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)