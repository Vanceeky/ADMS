from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
  
    

app_name = "authentication"
urlpatterns = [
  #  path('login/', views.login_page, name="login-page"),
    path('register/', views.register_page, name="register-page"),
    #path('password/reset/', views.reset_password, name="reset-password"),

    path('register-user/', views.register_user, name="register-user"),
    path('register-employee/', views.register_employee, name="register-employee"),

    path('login-user/', views.login_user, name="login-user"),
    path('logout/', views.logout_user, name="logout-user"),

    path('get_login_redirect_url/', views.get_login_redirect_url, name='get_login_redirect_url'),

    path('reset-password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
