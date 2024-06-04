from datetime import timezone
from django.forms import ValidationError
from django.shortcuts import render, redirect

from authentication.models import *
from django.http import JsonResponse
from django.db.models import Q
from base.models import *
from django.contrib import messages

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

def dean_dashboard(request):

    department = Department.objects.get(dean = request.user)
    courses = Course.objects.filter(department = department)
    IPrequest = IPMarkRemovalRequest.objects.filter(dean = department.dean)

    context = {
        'IPrequest': IPrequest,
        'courses': courses,
        'department': department,
    }

    return render(request, 'base/dean_dashboard.html', context)