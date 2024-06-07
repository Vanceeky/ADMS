from datetime import timezone
from django.forms import ValidationError
from django.shortcuts import render, redirect

from authentication.models import *
from django.http import JsonResponse
from django.db.models import Q
from base.models import *
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.


#STUDENT VIEWS
def dashboard(request):
    student = Student.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(student = student)

    context = {
        'IPrequest': IPrequest,
    }

    return render(request, 'base/dashboard.html', context)

def request_page(request):

    return render(request, 'base/request_page.html')


def request_process_page(request):
    return render(request, 'base/request_process.html')

def request_approved_page(request):
    return render(request, 'base/request_approved.html')


def user_dashboard(request):
    return render(request, 'base/user_dashboard.html')


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

        return redirect('base:request-page')

    

####################################################################################

#FACULTY VIEWS
def faculty_dashboard(request):
    faculty = Employee.objects.get(user = request.user)
    IPrequest = IPMarkRemovalRequest.objects.filter(instructor = faculty)
    additionalFile = AdditionalFile.objects.filter(request__in = IPrequest)



    context = {
        'IPrequest': IPrequest,
        'additionalFiles': additionalFile
    }




    return render(request, 'base/faculty_dashboard.html', context)



def submitIPMark(request):
    if request.method == 'POST':
        request_id = request.POST.get('requestID')

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

    approved_dean = IPrequest.filter(approved_by_dean = True)
    pending_dean = IPrequest.filter(approved_by_dean = False)


    students = Student.objects.filter(course = course)
    employees = Employee.objects.filter(department = department)

    context = {
        'IPrequest': IPrequest,
        'department': department,
        'students': students,
        'employees': employees,

        'approved_dean': approved_dean,
        'pending_dean': pending_dean

    }

    return render(request, 'base/dean_dashboard.html', context)


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









##############################################################

def acad_dashboard(request):
    #IPrequest = IPMarkRemovalRequest.objects.all()

    IPrequest = IPMarkRemovalRequest.objects.prefetch_related('additionalfile_set', 'ipmark_set').all()
    pending_request = IPrequest.filter(approved_by_ACAD = False)
    approved_request = IPrequest.filter(approved_by_ACAD = True)

    context = {
        'IPrequest': IPrequest,
        'pending_request': pending_request,
        'approved_request': approved_request
    }
    return render(request, 'base/acad_dashboard.html', context)


import qrcode
from io import BytesIO
from datetime import datetime

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


def display_request_form(request, request_id):

    IPrequest = IPMarkRemovalRequest.objects.get(id = request_id)
    IPmarks = IPMark.objects.filter(request = IPrequest)
    context = {
        'ip': IPrequest,
        'marks' : IPmarks
    }
    return render(request, 'base/includes/IPform.html', context)

