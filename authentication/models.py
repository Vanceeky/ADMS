from django.db import models
from django.contrib.auth.models import User
from department.models import Course, Department
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=15, unique=True)
    year_level = models.CharField(max_length=10)
    avatar = models.ImageField(default='/avatars/avatar-default-icon.png',upload_to='avatars/', null=True, blank=True)
    proof_of_enrollment = models.FileField(upload_to='proofs/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=15, unique=True)
    avatar = models.ImageField(default='/avatars/avatar-default-icon.png',upload_to='avatars/', null=True, blank=True)
    proof_of_employment = models.FileField(upload_to='proofs/', null=True, blank=True)

    def __str__(self):
        return self.user.username