
from django.forms import ValidationError
from django.shortcuts import render, redirect

from authentication.models import *
from django.http import JsonResponse
from django.db.models import Q
from base.models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
import json
from datetime import datetime, timedelta
# Create your views here.
from django.utils.timezone import now
from department.models import File
import qrcode
from io import BytesIO

from django.contrib.messages import success
#from datetime import datetime

#STUDENT VIEWS


def recent_activities(request, student):

    today = now().date()

    yesterday = today - timedelta(days=1)

    approval_statuses = {
        'approved_by_faculty_today': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_faculty=True,
            date_updated__date=today
        ),
        'approved_by_faculty_yesterday': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_faculty=True,
            date_updated__date=yesterday
        ),

        'approved_by_dean_today': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_dean=True,
            date_updated__date=today
        ),
        'approved_by_dean_yesterday': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_dean=True,
            date_updated__date=yesterday
        ),

        'approved_by_ACAD_today': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_ACAD=True,
            date_updated__date=today
        ),
        'approved_by_ACAD_yesterday': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_ACAD=True,
            date_updated__date=yesterday
        ),

        'approved_by_registrar_today': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_registrar=True,
            date_updated__date=today
        ),
        'approved_by_registrar_yesterday': IPMarkRemovalRequest.objects.filter(
            student=student,
            approved_by_registrar=True,
            date_updated__date=yesterday
        ),
    }

    return approval_statuses


def student_profile(request):
    student = Student.objects.get(user = request.user)
    context = {
        'student': student
    }
    return render(request, 'base/student/profile.html', context)



def dashboard(request):
    student = Student.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(student = student).prefetch_related('additionalfile_set', 'ipmark_set')

    approval_statuses = recent_activities(request, student)
    
    context = {
        'IPrequest': IPrequest,
        'approval_statuses': approval_statuses
    }

    return render(request, 'base/student/base.html', context)

def request_home(request):
    student = Student.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(student = student)

    approval_statuses = recent_activities(request, student)
    
    context = {
        'IPrequest': IPrequest,
        'approval_statuses': approval_statuses
    }

    return render(request, 'base/student/home.html', context)



def request_page(request):

    student = Student.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(student = student, status = 'Pending')
    approval_statuses = recent_activities(request, student)
    
    context = {
        'IPrequest': IPrequest,
        'approval_statuses': approval_statuses
    }
    return render(request, 'base/student/request_page.html', context)


def request_process_page(request):
    student = Student.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(student = student, status = 'Processing')
    approval_statuses = recent_activities(request, student)
    
    context = {
        'IPrequest': IPrequest,
        'approval_statuses': approval_statuses
    }
    return render(request, 'base/student/request_process.html', context)

def request_approved_page(request):
    student = Student.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(student = student, status = 'Approved')
    approval_statuses = recent_activities(request, student)
    
    context = {
        'IPrequest': IPrequest,
        'approval_statuses': approval_statuses
    }
    return render(request, 'base/student/request_approved.html', context)



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def instructors_autocomplete(request):
    if is_ajax(request=request):
        term = request.GET.get('term', '')
    
        results = Employee.objects.filter(
            Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term)
        ).values('user__first_name', 'user__last_name', 'employee_id') 

       
        suggestions = [
            {
                'name': f"{result['user__first_name']} {result['user__last_name']}",
                'id': result['employee_id']
            }
            for result in results
        ]

        return JsonResponse(suggestions, safe=False)
    else:
        return JsonResponse({'message': 'Not a valid request.'}, safe=False)

def requestIPMarkRemoval(request):
    if request.method == 'POST':
        student = request.POST.get('student')
        department = request.POST.get('department')  # Assuming department is still used
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        units = request.POST.get('units')
        sem_year = request.POST.get('sem_year')
        instructor = request.POST.get('instructor_id')

        # Get student and instructor objects
        student = Student.objects.get(id=student)
        instructor = Employee.objects.get(employee_id=instructor)
        department = Department.objects.get(id=department)  # Assuming department is still used

        # Create the IPMarkRemovalRequest object
        request_object = IPMarkRemovalRequest.objects.create(
            student=student,
            subject_code=subject_code,
            subject_name=subject_name,
            units=units,
            sem_year=sem_year,
            instructor=instructor,
            dean=department.dean  # Assuming department is still used
        )

        # Handle uploaded additional files
        if request.FILES.getlist('additional_file'):
            for uploaded_file in request.FILES.getlist('additional_file'):
                # Create an AdditionalFile object for each uploaded file
                AdditionalFile.objects.create(request=request_object, file=uploaded_file)


        return HttpResponse(json.dumps({"message": "Request submitted successfully"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Invalid request method"}), status=400, content_type="application/json")




    

####################################################################################

#FACULTY VIEWS

def faculty_dashboard(request):
    faculty = Employee.objects.get(user = request.user)
   # IPrequest = IPMarkRemovalRequest.objects.filter(instructor = faculty)
   # additionalFile = AdditionalFile.objects.filter(request__in = IPrequest)
    IPrequest = IPMarkRemovalRequest.objects.filter(instructor = faculty ).prefetch_related('additionalfile_set', 'ipmark_set')
    myRequest = FacultyLeaveOfAbsence.objects.filter(faculty = faculty)


    context = {
        'IPrequest': IPrequest,
        'myRequest': myRequest,
      #  'additionalFiles': additionalFile
    }


    return render(request, 'base/faculty/faculty_dashboard.html', context)


def faculty_course_guide(request):
   faculty = Employee.objects.get(user = request.user)
   course_guides = CourseGuide.objects.filter(faculty = faculty )

   context = {
      'course_guides': course_guides
   }
   return render(request, 'base/faculty/course_guide.html', context)


def faculty_submit_course_guide(request):
    faculty = Employee.objects.get(user=request.user)

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        file = request.FILES.get('file')

        try:
            course_guide = CourseGuide.objects.create(
                faculty=faculty,
                department=faculty.department,
                subject_name=subject_name,
                subject_code=subject_code,
                year=year,
                semester=semester,
                file=file,
                dean=faculty.department.dean,
            )

            course_guide.save()
            messages.success(request, 'Course guide submitted successfully.')
            return redirect('base:faculty-course-guide')

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('base:faculty-course-guide-form')  # Redirect to form on error

    return redirect('base:faculty-dashboard')  # Redirec


def faculty_student_requests_base(request):
    faculty = Employee.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(instructor = faculty).prefetch_related('additionalfile_set', 'ipmark_set')

    context = {
        'IPrequest': IPrequest
    }
    return render(request, 'base/faculty/base.html', context)
    


def get_ip_requests_by_status(request, status):
  faculty = Employee.objects.get(user=request.user)
  IPrequest = IPMarkRemovalRequest.objects.filter(instructor=faculty, status=status).prefetch_related('additionalfile_set', 'ipmark_set')
  return IPrequest

def faculty_student_requests_pending(request):
  IPrequest = get_ip_requests_by_status(request, 'Pending')
  context = {'IPrequest': IPrequest}
  return render(request, 'base/faculty/pending.html', context)

def faculty_student_requests_processing(request):
  IPrequest = get_ip_requests_by_status(request, 'Processing')
  context = {'IPrequest': IPrequest}
  return render(request, 'base/faculty/processing.html', context)

def faculty_student_requests_approved(request):
  IPrequest = get_ip_requests_by_status(request, 'Approved')
  context = {'IPrequest': IPrequest}
  return render(request, 'base/faculty/approved.html', context)


def faculty_leave_request(request):
    faculty = Employee.objects.get(user=request.user)
    LeaveRequest = FacultyLeaveOfAbsence.objects.filter(faculty = faculty)
    context = {
        'LeaveRequest': LeaveRequest
    }
    return render(request, 'base/faculty/leave_request.html', context)




def submit_leave_request(request):
    faculty = Employee.objects.get(user=request.user)
    department = faculty.department
    dean = department.dean

    if request.method == 'POST':
        purpose_of_absence = request.POST.get('purpose_of_absence')
        start_date = request.POST.get('from_date')
        end_date = request.POST.get('to_date')
        number_of_days = request.POST.get('number_of_days')
        reason = request.POST.get('reason')
        length_of_service = request.POST.get('lengthOfService')
        is_there_substitute = request.POST.get('is_there_substitute', False)  # Default to False if not checked
        name_of_substitute = request.POST.get('name_of_substitute')
        substitute_reason = None

        if is_there_substitute:
            substitute_reason = request.POST.get('substitute_reason')

        try:
            my_request = FacultyLeaveOfAbsence.objects.create(
                faculty=faculty,
                purpose=purpose_of_absence,
                from_date=start_date,
                to_date=end_date,
                number_of_days=number_of_days,
                reason=reason,
                lengthOfService=length_of_service,
                is_there_substitute=is_there_substitute,
                name_of_substitute=name_of_substitute,
                reason_for_substitute=substitute_reason,
                dean=dean,
                department=department,
            )

            my_request.save()
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('base:faculty-leave-requests')

        except Exception as e:  # Catch generic exception for broader error handling
            messages.error(request, f'An error occurred: {e}')
            return redirect('base:faculty-leave-requests')  # Redirect to form on error

    return redirect('base:faculty-leave-requests')  # Redirect to dashboard on GET request



def faculty_pending_request(request):

    pass 


def submitIPMark(request):
    if request.method == 'POST':
        request_id = request.POST.get('requestID')

        try:
            ip_request = IPMarkRemovalRequest.objects.get(id=request_id)

            prelim = request.POST.get('prelim')
            midterm = request.POST.get('midterm')
            semis = request.POST.get('semis')
            finals = request.POST.get('finals')
            final_grade = request.POST.get('final_grade')
            remarks = request.POST.get('remarks')

            IpMark = IPMark.objects.create(
                request=ip_request,
                prelim=prelim,
                midterm=midterm,
                semis=semis,
                finals=finals,
                final_grade=final_grade,
                remarks=remarks
            )

            ip_request.approved_by_faculty = True
            ip_request.status = 'Processing'

            ip_request.save()
            IpMark.save()

            # Add success message with Django messages framework
            success(request, 'IP mark for request ID {} has been submitted successfully.'.format(request_id))

            return redirect('base:faculty-student-requests')

        except IPMarkRemovalRequest.DoesNotExist:
            # Handle case where request_id is not found (optional)
            error_message = 'The specified IP mark removal request could not be found.'
            return render(request, 'base/error.html', context={'message': error_message})

    return redirect('base:faculty-dashboard')
    




####################################################################################
#DEAN Views


def dean_profile(request):
    return render(request, 'base/dean_profile.html')


def dean_dashboard(request):

    department = Department.objects.get(dean = request.user)
    course = Course.objects.get(department = department)
   # IPrequest = IPMarkRemovalRequest.objects.filter(dean = department.dean)
    IPrequest = IPMarkRemovalRequest.objects.filter(dean=department.dean).prefetch_related('additionalfile_set', 'ipmark_set')
    leaveRequest = FacultyLeaveOfAbsence.objects.filter(dean = department.dean)


    approved_dean = IPrequest.filter(approved_by_dean = True)
    pending_dean = IPrequest.filter(approved_by_dean = False)

    leave_pending = leaveRequest.filter(approved_by_dean = False)
    leave_approved = leaveRequest.filter(approved_by_dean = True)



    students = Student.objects.filter(course = course)
    employees = Employee.objects.filter(department = department)

    context = {
        'IPrequest': IPrequest,
        'leaveRequest': leaveRequest,

        'department': department,
        'students': students,
        'employees': employees,

        'approved_dean': approved_dean,
        'pending_dean': pending_dean,

        'leave_pending': leave_pending,
        'leave_approved': leave_approved,

    }

    return render(request, 'base/dean/dean_dashboard.html', context)


def dean_faculty(request):
    return render(request, 'base/dean_faculty.html')

def dean_students(request):

    department = Department.objects.get(dean = request.user)
    course = Course.objects.get(department = department)
    students = Student.objects.filter(course = course)
    context = {
        'students': students,
    }
    return render(request, 'base/students.html', context)


def approved_IP_request(request, request_id):
    IPrequest = IPMarkRemovalRequest.objects.get(id = request_id)
    IPrequest.approved_by_dean = True
    IPrequest.save()

    return redirect('base:dean-dashboard')

def approve_leave_request_dean(request, request_id):
    leaveRequest = FacultyLeaveOfAbsence.objects.get(id = request_id)
    leaveRequest.approved_by_dean = True
    leaveRequest.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def accept_user(request, user_id):
    user = User.objects.get(id = user_id)
    user.is_active = True
    user.save()

    # Email notification content
    subject = 'Lyceum Account Activated'
    message = f"""
    Hi {user.first_name} {user.last_name},

    Your account at Lyceum has been successfully activated.

    You can now log in using your credentials.
    
    
    Username: {user.username}
    Password: {user.username}
    Email: {user.email}

    Thank you for choosing Lyceum!

    Sincerely,
    Lyceum Registration Team
    """

    # Send email notification to the user
    send_mail(
        subject,
        message,
        'noreply@lyceum.edu.ph', 
        [user.email],
        fail_silently=False,
    )
    return redirect('base:dean-dashboard')


def dean_ip_base(request):
    dean = request.user
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_faculty = True, dean = dean)
    approved_dean = IPrequest.filter(approved_by_dean = True)
    pending_dean = IPrequest.filter(approved_by_dean = False)

    leaveRequest = FacultyLeaveOfAbsence.objects.filter(dean = dean)

    leave_pending = leaveRequest.filter(approved_by_dean = False)
    leave_approved = leaveRequest.filter(approved_by_dean = True)


    context = {
        'IPrequest': IPrequest,
        'approved_dean': approved_dean,
        'pending_dean': pending_dean,

        'leave_pending': leave_pending,
        'leave_approved': leave_approved,
    }
    return render(request, 'base/dean/ip_base.html', context)

def dean_ip_pending(request):
    dean = request.user
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_dean = False, dean = dean)
    context = {
        'IPrequest': IPrequest
    }
    return render(request, 'base/dean/ip_pending.html', context)

def dean_ip_approved(request):
    dean = request.user
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_dean = True, dean = dean)
    context = {
        'IPrequest': IPrequest
    }
    return render(request, 'base/dean/ip_approved.html', context)




def dean_leave_base(request):
    dean = request.user 
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_faculty = True, dean = dean)
    approved_dean = IPrequest.filter(approved_by_dean = True)
    pending_dean = IPrequest.filter(approved_by_dean = False)

    leaveRequest = FacultyLeaveOfAbsence.objects.filter(dean = dean)

    leave_pending = leaveRequest.filter(approved_by_dean = False)
    leave_approved = leaveRequest.filter(approved_by_dean = True)

    context = {
        'leaveRequest': leaveRequest,

        'approved_dean': approved_dean,
        'pending_dean': pending_dean,

        'leave_pending': leave_pending,
        'leave_approved': leave_approved,

    }
    return render(request, 'base/dean/leave_base.html', context)



def dean_leave_pending(request):
  dean = request.user
  leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_dean = False, dean = dean)

  context = {
      'leaveRequest': leaveRequest,
  }
  return render(request, 'base/dean/leave_pending.html', context)

def dean_leave_approved(request):
  dean = request.user
  leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_dean = True, dean = dean)

  context = {
      'leaveRequest': leaveRequest,
  }
  return render(request, 'base/dean/leave_approved.html', context)




def dean_course_guide(request):
    dean = request.user
    department = Department.objects.get(dean = dean)
    course_guides = CourseGuide.objects.filter(department = department)
    course = Course.objects.get(department = department)
   # IPrequest = IPMarkRemovalRequest.objects.filter(dean = department.dean)
    IPrequest = IPMarkRemovalRequest.objects.filter(dean=department.dean).prefetch_related('additionalfile_set', 'ipmark_set')
    leaveRequest = FacultyLeaveOfAbsence.objects.filter(dean = department.dean)


    approved_dean = IPrequest.filter(approved_by_dean = True)
    pending_dean = IPrequest.filter(approved_by_dean = False)

    leave_pending = leaveRequest.filter(approved_by_dean = False)
    leave_approved = leaveRequest.filter(approved_by_dean = True)



    students = Student.objects.filter(course = course)
    employees = Employee.objects.filter(department = department)

    context = {
        'course_guides': course_guides,
        'students': students,
        'employees': employees,

        'approved_dean': approved_dean,
        'pending_dean': pending_dean,

        'leave_pending': leave_pending,
        'leave_approved': leave_approved,
    }
    return render(request, 'base/dean/course_guide.html', context)



def upload_dept_file(request):
     if request.method == 'POST':
        name = request.POST.get('file_name')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        dept_file = File.objects.create(
          name = name,
          description = description,
          department = request.user.department,
          file = file
        )

        dept_file.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def dean_delete_file(request, request_id):
    file = File.objects.get(id = request_id)
    file.delete()
    return redirect('base:dean-files')

def dean_files(request):
    files = File.objects.filter(department = request.user.department)

    context = {
        'files': files
    }
    return render(request, 'base/dean/files.html', context)


def dean_approve_course_guide(request, request_id):
    course_guide = CourseGuide.objects.get(id = request_id)
    course_guide.approved_by_dean = True
    course_guide.status = 'Approved'
    course_guide.save()

    return redirect('base:dean-course-guide')




##############################################################

def acad_dashboard(request):
    #IPrequest = IPMarkRemovalRequest.objects.all()

    IPrequest = IPMarkRemovalRequest.objects.prefetch_related('additionalfile_set', 'ipmark_set').all()
    pending_request = IPrequest.filter(approved_by_dean = True, approved_by_ACAD = False)
    approved_request = IPrequest.filter(approved_by_dean = True, approved_by_ACAD = True)

    leaveRequest = FacultyLeaveOfAbsence.objects.all()

    context = {
        'IPrequest': IPrequest,
        'pending_request': pending_request,
        'approved_request': approved_request,

        'leave_pending': leaveRequest.filter(approved_by_ACAD = False, approved_by_dean = True),
        'leave_approved': leaveRequest.filter(approved_by_ACAD = True, approved_by_dean = True),

        'leaveRequest': leaveRequest
    }
    return render(request, 'base/acad/acad_dashboard.html', context)

def approved_request_acad(request, request_id):

    IPrequest = IPMarkRemovalRequest.objects.get(id=request_id)

    # Update model fields
    IPrequest.acad = request.user
    IPrequest.approved_by_ACAD = True
    IPrequest.status = 'Approved'

    # Generate QR code data
    acad_name = f"{IPrequest.acad.first_name} {IPrequest.acad.last_name}"  # Assuming first_name and last_name exist for User model
    approved_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formatted date and time
    qr_data = f"IP Mark Removal Request Approved by: {acad_name} on {approved_datetime}"

    # Create QR code image in memory
    img_buffer = BytesIO()
    qr = qrcode.QRCode(
        version=1,  # Adjust version for complexity/size balance (optional)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Adjust error correction (optional)
        box_size=10,  # Adjust box size for image size (optional)
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_buffer, format="PNG")

    # Update IPrequest.qr with generated image data
    IPrequest.qr_code.save(f"{approved_datetime}.png", BytesIO(img_buffer.getvalue()), save=False)

    # Save updated model instance
    IPrequest.save()

    return redirect('base:acad-dashboard')

def approve_leave_request(request, request_id):

    leaveRequest = FacultyLeaveOfAbsence.objects.get(id=request_id)
    leaveRequest.acad = request.user
    leaveRequest.approved_by_ACAD = True
    leaveRequest.status = 'Approved'

    # Generate QR code data
    acad_name = f"{leaveRequest.acad.first_name} {leaveRequest.acad.last_name}"  # Assuming first_name and last_name exist for User model
    approved_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formatted date and time
    qr_data = f"Faculty Leave of Absence Approved by: {acad_name} on {approved_datetime}"

    # Create QR code image in memory
    img_buffer = BytesIO()
    qr = qrcode.QRCode(
        version=1,  # Adjust version for complexity/size balance (optional)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Adjust error correction (optional)
        box_size=10,  # Adjust box size for image size (optional)
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_buffer, format="PNG")

    # Update IPrequest.qr with generated image data
    leaveRequest.qr_code.save(f"{approved_datetime}.png", BytesIO(img_buffer.getvalue()), save=False)

    # Save updated model instance
    leaveRequest.save()

    return redirect('base:acad-dashboard')


def display_request_form(request, request_id):

    IPrequest = IPMarkRemovalRequest.objects.get(id = request_id)
    IPmarks = IPMark.objects.filter(request = IPrequest)
    context = {
        'ip': IPrequest,
        'marks' : IPmarks
    }
    return render(request, 'base/includes/IPform.html', context)


"""
def ip_base(request):
    IPrequest = IPMarkRemovalRequest.objects.prefetch_related('additionalfile_set', 'ipmark_set').all()
    pending_request = IPrequest.filter(approved_by_dean = True, approved_by_ACAD = False)
    approved_request = IPrequest.filter(approved_by_dean = True, approved_by_ACAD = True)

    leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_dean = True)

    context = {
        'IPrequest': IPrequest,
        'pending_request': pending_request,
        'approved_request': approved_request,

        'leave_pending': leaveRequest.filter(approved_by_ACAD = False, approved_by_dean = True),
        'leave_approved': leaveRequest.filter(approved_by_ACAD = True, approved_by_dean = True),
    }
    return render(request, 'base/acad/ip_base.html', context)

def ip_pending(request):
    IPrequest = IPMarkRemovalRequest.objects.prefetch_related('additionalfile_set', 'ipmark_set').all()
    pending_request = IPrequest.filter(approved_by_ACAD = False)
    approved_request = IPrequest.filter(approved_by_ACAD = True)

    context = {
        'IPrequest': IPrequest,
        'pending_request': pending_request,
        'approved_request': approved_request,
    }
    return render(request, 'base/acad/ip_pending.html', context)

def ip_approved(request):
    IPrequest = IPMarkRemovalRequest.objects.prefetch_related('additionalfile_set', 'ipmark_set').all()
    pending_request = IPrequest.filter(approved_by_ACAD = False)
    approved_request = IPrequest.filter(approved_by_ACAD = True)

    context = {
        'IPrequest': IPrequest,
        'pending_request': pending_request,
        'approved_request': approved_request,


    }
    return render(request, 'base/acad/ip_approved.html', context)
"""

def get_ip_requests(request, approved_by_acad=None):
  filters = {'approved_by_dean': True}
  if approved_by_acad is not None:
    filters['approved_by_ACAD'] = approved_by_acad
  IPrequest = IPMarkRemovalRequest.objects.prefetch_related('additionalfile_set', 'ipmark_set').filter(**filters)
  return IPrequest

def ip_base(request):
  IPrequest = get_ip_requests(request)  # All (approved by Dean)
  pending_request = get_ip_requests(request, approved_by_acad=False)
  approved_request = get_ip_requests(request, approved_by_acad=True)

  leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_dean=True)

  context = {
      'IPrequest': IPrequest,
      'pending_request': pending_request,
      'approved_request': approved_request,
      'leave_pending': leaveRequest.filter(approved_by_ACAD=False, approved_by_dean=True),
      'leave_approved': leaveRequest.filter(approved_by_ACAD=True, approved_by_dean=True),
  }
  return render(request, 'base/acad/ip_base.html', context)

def ip_pending(request):
  IPrequest = get_ip_requests(request, approved_by_acad=False)
  pending_request = IPrequest
  approved_request = []  # Empty list for approved

  context = {
      'IPrequest': IPrequest,
      'pending_request': pending_request,
      'approved_request': approved_request,
  }
  return render(request, 'base/acad/ip_pending.html', context)

def ip_approved(request):
  IPrequest = get_ip_requests(request, approved_by_acad=True)
  pending_request = []  # Empty list for pending
  approved_request = IPrequest

  context = {
      'IPrequest': IPrequest,
      'pending_request': pending_request,
      'approved_request': approved_request,
  }
  return render(request, 'base/acad/ip_approved.html', context)


def get_leave_requests(request, approved_by_acad=None):
  filters = {'approved_by_dean': True}
  if approved_by_acad is not None:
    filters['approved_by_ACAD'] = approved_by_acad
  leaveRequest = FacultyLeaveOfAbsence.objects.filter(**filters)
  return leaveRequest



def leave_base(request):
  leaveRequest = get_leave_requests(request)  # All (approved by Dean)
  context = {
      'leaveRequest': leaveRequest,
      'leave_pending': get_leave_requests(request, approved_by_acad=False),
      'leave_approved': get_leave_requests(request, approved_by_acad=True),
  }
  return render(request, 'base/acad/leave_base.html', context)

def leave_pending(request):
  leaveRequest = get_leave_requests(request, approved_by_acad=False)
  context = {
      'leaveRequest': leaveRequest,
  }
  return render(request, 'base/acad/leave_pending.html', context)

def leave_approved(request):
  leaveRequest = get_leave_requests(request, approved_by_acad=True)
  context = {
      'leaveRequest': leaveRequest,
  }
  return render(request, 'base/acad/leave_approved.html', context)


def acad_departments(request):
    departments = Department.objects.all()
    # Fetch related models for each department
    department_data = []
    for department in departments:
        courses = department.course_set.all()
        employees = department.employee_set.all()
        
        # Fetch students through courses
        students = Student.objects.filter(course__in=courses)

        department_data.append({
            'department': department,
            'courses': courses,

            'num_employees': employees.count(),  # Count of employees
            'num_students': students.count(),    # Count of students
        })

    context = {
        'department_data': department_data
    }
    
    return render(request, 'base/acad/departments.html', context)

def department_page(request, dept_id):
    department = Department.objects.get(pk=dept_id)
    files = File.objects.filter(department = department)
    # Retrieve related models
    courses = department.course_set.all()
    course_guides = department.courseguide_set.all()
    employees = department.employee_set.all()

    # Fetch students through courses
    students = Student.objects.filter(course__in=courses)

    context = {
        'department': department,
        'courses': courses,
        'course_guides': course_guides,
        'employees': employees,
        'students': students,
        'files': files
    }
    return render(request, 'base/acad/department_page.html', context)

def acad_approve_course_guide(request, course_guide_id):
    course_guide = CourseGuide.objects.get(pk=course_guide_id)
    course_guide.approved_by_ACAD = True
    course_guide.acad = request.user
    course_guide.status = 'Approved'
    course_guide.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




#REGISTRAR VIEWS

def registrar_home(request):
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_ACAD = True)
    context = {
        'IPrequest': IPrequest
    }
    return render(request, 'base/registrar/home.html', context)

def registrar_pending_ip(request):
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_registrar = False)
    context = {
        'IPrequest': IPrequest
    }
    return render(request, 'base/registrar/pending.html', context)

def registrar_received_ip(request):
    IPrequest = IPMarkRemovalRequest.objects.filter(approved_by_registrar = True)
    context = {
        'IPrequest': IPrequest
    }
    return render(request, 'base/registrar/received.html', context)

def registrar_receive_ip_request(request, request_id):
    IPrequest = IPMarkRemovalRequest.objects.get(id = request_id)
    IPrequest.approved_by_registrar = True
    IPrequest.registrar = request.user
    IPrequest.status = 'Approved'
    IPrequest.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



def hr_home(request):
    leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_ACAD = True)
    context = {
        'leaveRequest': leaveRequest
    }
    return render(request, 'base/hr/home.html', context)

def hr_pending_leave(request):
    leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_HR = False)
    context = {
        'leaveRequest': leaveRequest
    }
    return render(request, 'base/hr/pending.html', context)

def hr_approved_leave(request):
    leaveRequest = FacultyLeaveOfAbsence.objects.filter(approved_by_HR = True)
    context = {
        'leaveRequest': leaveRequest
    }
    return render(request, 'base/hr/approved.html', context)

def hr_approve_leave_request(request, request_id):
    leaveRequest = FacultyLeaveOfAbsence.objects.get(id = request_id)
    leaveRequest.approved_by_HR = True
    leaveRequest.hr = request.user
    leaveRequest.status = 'Approved'
    leaveRequest.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def display_leave_request_form(request, request_id):

    leaveRequest = FacultyLeaveOfAbsence.objects.get(id = request_id)

    context = {
        'leaveRequest': leaveRequest
    }
    return render(request, 'base/includes/leaveForm.html', context)

