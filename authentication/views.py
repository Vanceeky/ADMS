from django.shortcuts import render

# Create your views here.

def login_user(request):
    return render(request, 'authentication/sign-in.html')

def register_user(request):
    return render(request, 'authentication/sign-up.html')

def reset_password(request):
    return render(request, 'authentication/reset_password.html')