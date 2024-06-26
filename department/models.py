from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null = True, blank = True)
    dean = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.department}'
    
class File(models.Model):
    file_type = models.CharField(max_length = 155, null = True, blank = True, name="file_type")
    name = models.CharField(max_length = 155)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null = True, blank = True)
    file = models.FileField(upload_to='files/')

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

