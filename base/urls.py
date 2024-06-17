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
    path('student/account/', views.student_profile, name="student-profile"),



    #Faculty URLS
    path('faculty/home/', views.faculty_dashboard, name='faculty-dashboard'),
    path('faculty/student-requests/', views.faculty_student_requests_base, name="faculty-student-requests"),
    path('faculty/student-requests/pending/', views.faculty_student_requests_pending, name="faculty-student-requests-pending"),
    path('faculty/student-requests/processing/', views.faculty_student_requests_processing, name="faculty-student-requests-processing"),
    path('faculty/student-requests/approved/', views.faculty_student_requests_approved, name="faculty-student-requests-approved"),

    path('faculty/leave/requests/', views.faculty_leave_request, name='faculty-leave-requests'),

    path('faculty/course-guide/', views.faculty_course_guide, name='faculty-course-guide'),
    path('faculty/upload-course-guide/', views.faculty_submit_course_guide, name='faculty-submit-course-guide'),


    path('submit/leave-request/', views.submit_leave_request, name='submit-leave-request'),
    path('submit-IP-Mark/', views.submitIPMark, name='submit-IP-Mark'),


    #BASE urls
    path('instructors-autocomplete/', views.instructors_autocomplete, name='instructors-autocomplete'),




    #DEAN URLS
    path('dean/account/profile/', views.dean_profile, name='dean-profile'),
    
    path('dean/', views.dean_dashboard, name='dean-dashboard'),
    path('students/', views.dean_students, name='students'),

    path('approve-IPMarkRemoval-request/<int:request_id>/', views.approved_IP_request, name='approve-IPMarkRemoval-request'),
    path('approve-leave-request/dean/<str:request_id>/', views.approve_leave_request_dean, name='approve-leave-request-dean'),
    path('accept-user/<str:user_id>/', views.accept_user, name='accept-user'),



    path('dean/requests/ip/', views.dean_ip_base, name="dean-request-ip"),
    path('dean/requests/ip/pending/', views.dean_ip_pending, name="dean-request-ip-pending"),
    path('dean/requests/ip/approved/', views.dean_ip_approved, name="dean-request-ip-approved"),


    path('dean/requests/leave/', views.dean_leave_base, name="dean-request-leave"),
    path('dean/requests/leave/pending/', views.dean_leave_pending, name="dean-request-leave-pending"),
    path('dean/requests/leave/approved/', views.dean_leave_approved, name="dean-request-leave-approved"),

    path('dean/course-guides/', views.dean_course_guide, name='dean-course-guide'),
    path('dean/approve-course-guide/<str:request_id>/', views.dean_approve_course_guide, name='dean-approve-course-guide'),
    path('dean/department/files/', views.dean_files, name='dean-files'),
    path('dean/department/file/upload/', views.upload_dept_file, name='upload-dept-file'),
    path('dean/delete-file/<str:request_id>/', views.dean_delete_file, name='dean-delete-file'),

    #ACAD URLS
    path('acad/', views.acad_dashboard, name='acad-dashboard'),
    path('approve-ip-mark-removal-request/<str:request_id>/', views.approved_request_acad, name='approve-ip-mark-removal-request'),
    path('approve-leave-request/acad/<str:request_id>/', views.approve_leave_request, name='approve-leave-request-acad'),
    path('acad/approve-course-guide/<str:course_guide_id>/', views.acad_approve_course_guide, name='acad-approve-course-guide'),

    path('view/IP-approval-form/<str:request_id>/', views.display_request_form, name='view-approval-form'),

    path('acad/requests/ip/', views.ip_base, name="acad-request-ip"),
    path('acad/requests/ip/pending/', views.ip_pending, name="acad-request-ip-pending"),
    path('acad/requests/ip/approved/', views.ip_approved, name="acad-request-ip-approved"),

    path('acad/requests/leave/', views.leave_base, name="acad-request-leave"),
    path('acad/requests/leave/pending/', views.leave_pending, name="acad-request-leave-pending"),
    path('acad/requests/leave/approved/', views.leave_approved, name="acad-request-leave-approved"),

    path('acad/departments/', views.acad_departments, name="acad-departments"),
    path('acad/deparment/<str:dept_id>/', views.department_page, name="acad-department-detail"),

    path('registrar/', views.registrar_home, name='registrar-home'),
    path('registrar/pending/ip-mark-removal/', views.registrar_pending_ip, name='registrar-pending'),
    path('registrar/receieve/ip-mark-removal/', views.registrar_received_ip, name='registrar-received'),
    path('registrar/receieve/ip-mark-removal-request/<str:request_id>/', views.registrar_receive_ip_request, name='registrar-receive-ip-request'),


    #HR URLS
    path('hr/', views.hr_home, name='hr-home'),
    path('hr/pending/leave/', views.hr_pending_leave, name='hr-pending-leave'),
    path('hr/approved/leave/', views.hr_approved_leave, name='hr-approved-leave'),
    path('hr/approve/leave/<str:request_id>/', views.hr_approve_leave_request, name='hr-approve-leave-request'),
    path('faculty/leave/request/<str:request_id>/', views.display_leave_request_form, name='faculty-leave-request-form'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)