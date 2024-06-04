from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path('login/', views.login_page, name="login-page"),
    path('register/', views.register_page, name="register-page"),
    path('reset-password/', views.reset_password, name="reset-password"),

    path('register-user/', views.register_user, name="register-user"),
    path('register-employee/', views.register_employee, name="register-employee"),

    path('login-user/', views.login_user, name="login-user"),
    path('logout/', views.logout_user, name="logout-user"),
]
