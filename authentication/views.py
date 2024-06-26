from django.shortcuts import render, redirect
from department.models import Course, Department
from django.contrib.auth.models import User, Group
from . models import Student, Employee

from django.contrib import messages 
from django.db import IntegrityError
from django.http import JsonResponse

from django.core.mail import send_mail
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from base.decorators import prevent_logged_in_users

# Create your views here.

def login_page(request):
    return render(request, 'authentication/sign-in.html')

from django.urls import reverse

@login_required
def get_login_redirect_url(request):
    user = request.user
    if user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))
    elif user.groups.filter(name='student').exists():
        return HttpResponseRedirect(reverse('base:student-dashboard'))
    elif user.groups.filter(name='faculty').exists():
        return HttpResponseRedirect(reverse('base:faculty-dashboard'))
    elif user.groups.filter(name='dean').exists():
        return HttpResponseRedirect(reverse('base:dean-dashboard'))
    elif user.groups.filter(name='acad').exists():
        return HttpResponseRedirect(reverse('base:acad-dashboard'))
    elif user.groups.filter(name='registrar').exists():
        return HttpResponseRedirect(reverse('base:registrar-home'))
    elif user.groups.filter(name='hr').exists():
        return HttpResponseRedirect(reverse('base:hr-home'))
    else:
        return HttpResponseRedirect(reverse('base:default-dashboard'))
    

    
    


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, password=password)
        except PermissionError:  # Handle potential permission errors (optional)
            messages.error(request, 'An unexpected error occurred during login.')
            return render(request, 'authentication/sign-in.html')
        
        # Check user authentication
        if user is not None:
            if user.is_active:
                login(request, user)

                # Group redirection logic
                student_group = Group.objects.get(name="student")
                faculty_group = Group.objects.get(name='faculty')

                if user.groups.filter(name='student').exists():
                    return redirect('base:student-dashboard')
                elif user.groups.filter(name='faculty').exists():
                    return redirect('base:faculty-dashboard')
                elif user.groups.filter(name='dean').exists():
                    return redirect('base:dean-dashboard')
                else:
                    # Handle unexpected scenario where user isn't in either group
                    messages.warning(request, 'Your account is not associated with a known group. Please contact the administrator.')
                    return redirect('authentication:login-page')
            elif user.is_active is False:
                # User is inactive, display message
                messages.warning(request, 'Your account is currently inactive. Please contact the administrator for approval.')
                # Implement your logic for approval workflow (e.g., redirect to approval page)
                # return redirect('approval:approval_page')  # Replace with your approval URL (if applicable)
        else:
            # Authentication failed (could be incorrect credentials)
            messages.info(request, 'Username or password is incorrect')

    return redirect('authentication:login-page')



def logout_user(request):
    logout(request)
    return redirect('/account/login')



@prevent_logged_in_users
def register_page(request):
    departments = Department.objects.all()
    courses = Course.objects.all()

    context = {
        'departments': departments,
        'courses': courses,
    }
    return render(request, 'authentication/sign-up.html', context)



def register_user(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        student_number = request.POST.get('student_number')
        year_level = request.POST.get('year_level')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        proof_of_enrollment = request.FILES.get('proof_of_enrollment')

        try:
            user = User.objects.create_user(
                username=student_number,
                email=email,
                first_name=firstname,
                last_name=lastname,
                password=student_number,
                is_active=False  # Set user inactive until approved
            )

            student = Student.objects.create(
                user=user,
                course=Course.objects.get(id=course),
                student_id=student_number,
                year_level=year_level,
                proof_of_enrollment=proof_of_enrollment
            )

            student.save()

            # Get the student group object
            student_group = Group.objects.get(name='student')

            # Add the user to the student group
            student_group.user_set.add(user)


            # Email notification content
            subject = 'Lyceum-AMDS Registration Confirmation'
            message = f"""
            Hi {firstname} {lastname},

            This email confirms that you have successfully registered for an account at Lyceum ADMS.

            Your login credentials are:
            Username: {student_number}
            Password: {student_number}
            Email: {email}

            **Please note:** Your account is currently inactive and awaits approval. You will be notified within 24 hours regarding the status of your registration.

            Thank you for choosing Lyceum!

            Sincerely,
            Lyceum Academic Affairs
            """

            # Send email notification to the registered user
            send_mail(
                subject,
                message,
                'noreply@lyceum.edu.ph',  # Replace with your sender email
                [email],
                fail_silently=False,
            )

            message = 'You will be notified within 24 hours regarding the approval status of your registration. A confirmation email has been sent to your provided address.'

            return JsonResponse({'success': True, 'message': message})

        except IntegrityError as e:
            return JsonResponse({'success': False, 'message': f'Registration failed: {e}'})

    return redirect('authentication:register-page')


def register_employee(request):
    if request.method == "POST":
        department = request.POST.get('department')
        employee_number = request.POST.get('employee_number')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        proof_of_employment = request.FILES.get('employee_id')

        try:
            user = User.objects.create_user(
                username=employee_number,
                email=email,
                first_name=firstname,
                last_name=lastname,
                password=employee_number,
                is_active=False  # Set user inactive until approved
            )

            employee = Employee.objects.create(
                user=user,
                department=Department.objects.get(id=department),
                employee_id=employee_number,
                proof_of_employment=proof_of_employment

            )

            employee.save()

            # Get the student group object
            faculty_group = Group.objects.get(name='faculty')  # Replace 'Students' with your actual group name

            # Add the user to the student group
            faculty_group.user_set.add(user)

            # Email notification content
            subject = 'Lyceum Registration Confirmation'
            message = f"""
            Hi {firstname} {lastname},

            This email confirms that you have successfully registered for an account at Lyceum.

            Your login credentials are:
            Username: {employee_number}
            Password: {employee_number}
            Email: {email}

            **Please note:** Your account is currently inactive and awaits approval. You will be notified within 24 hours regarding the status of your registration.

            Thank you for choosing Lyceum!

            Sincerely,
            Lyceum Registration Team
            """

            # Send email notification to the registered user
            send_mail(
                subject,
                message,
                'noreply@lyceum.edu.ph',  # Replace with your sender email
                [email],
                fail_silently=False,
            )

            message = 'You will be notified within 24 hours regarding the approval status of your registration. A confirmation email has been sent to your provided address.'

            message = 'You will be notified within 24 hours regarding the approval status of your registration.'

            return JsonResponse({'success': True, 'message': message})

        except IntegrityError as e:
            return JsonResponse({'success': False, 'message': f'Registration failed: {e}'})
        
    return redirect('authentication:register-page')


def reset_password(request):
    return render(request, 'authentication/reset_password.html')


