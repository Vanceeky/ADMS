from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'base'
urlpatterns = [

    #Student URLS
    path('', views.dashboard, name='student-dashboard'),
    path('request/dashboard/', views.request_home, name='request-home-page'),
    path('request/pending/', views.request_page, name='request-pending-page'),
    path('request/processing/', views.request_process_page, name='request-process-page'),
    path('request/approved/', views.request_approved_page, name='request-approved-page'),

    path('requestIPMarkRemoval/', views.requestIPMarkRemoval, name='requestIPMarkRemoval'),



    #Faculty URLS
    path('faculty/home/', views.faculty_dashboard, name='faculty-dashboard'),
    path('faculty/student-requests/', views.faculty_student_requests_base, name="faculty-student-requests"),
    path('faculty/student-requests/pending/', views.faculty_student_requests_pending, name="faculty-student-requests-pending"),
    path('faculty/student-requests/processing/', views.faculty_student_requests_processing, name="faculty-student-requests-processing"),
    path('faculty/student-requests/approved/', views.faculty_student_requests_approved, name="faculty-student-requests-approved"),

    path('faculty/leave/request/', views.faculty_leave_request, name='faculty-leave-requests'),
    path('faculty/leave/pending/', views.faculty_leave_request_pending, name='faculty-leave-pending'),
    path('faculty/leave/processing/', views.faculty_leave_request_processing, name='faculty-leave-processing'),
    path('faculty/leave/approved/', views.faculty_leave_request_approved, name='faculty-leave-approved'),




    path('submit/leave-request/', views.submit_leave_request, name='submit-leave-request'),
    path('submit-IP-Mark/', views.submitIPMark, name='submit-IP-Mark'),


    #BASE urls
    path('instructors-autocomplete/', views.instructors_autocomplete, name='instructors-autocomplete'),




    #DEAN URLS
    path('dean/account/profile/', views.dean_profile, name='dean-profile'),
    
    path('dean-dashboard/', views.dean_dashboard, name='dean-dashboard'),
    path('students/', views.dean_students, name='students'),

    path('approve-IPMarkRemoval-request/<int:request_id>/', views.approved_IP_request, name='approve-IPMarkRemoval-request'),
    path('approve-leave-request/dean/<str:request_id>/', views.approve_leave_request_dean, name='approve-leave-request-dean'),
    path('accept-user/<str:user_id>/', views.accept_user, name='accept-user'),


    #ACAD URLS
    path('acad/', views.acad_dashboard, name='acad-dashboard'),
    path('approve-ip-mark-removal-request/<str:request_id>/', views.approved_request_acad, name='approve-ip-mark-removal-request'),
    path('approve-leave-request/acad/<str:request_id>/', views.approve_leave_request, name='approve-leave-request-acad'),


    path('view/IP-approval-form/<str:request_id>/', views.display_request_form, name='view-approval-form'),

    path('acad/requests/ip/', views.ip_base, name="acad-request-ip"),
    path('acad/requests/ip/pending/', views.ip_pending, name="acad-request-ip-pending"),
    path('acad/requests/ip/approved/', views.ip_approved, name="acad-request-ip-approved"),

    path('acad/requests/leave/', views.leave_base, name="acad-request-leave"),
    path('acad/requests/leave/pending/', views.leave_pending, name="acad-request-leave-pending"),
    path('acad/requests/leave/approved/', views.leave_approved, name="acad-request-leave-approved"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)