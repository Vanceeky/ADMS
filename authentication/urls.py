from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path('login/', views.login_user, name="login-user"),
    path('register/', views.register_user, name="register-user"),
    path('reset-password/', views.reset_password, name="reset-password"),
]
