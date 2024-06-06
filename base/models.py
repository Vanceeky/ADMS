from django.db import models
from authentication.models import Student, Employee
from department.models import Department
from django.contrib.auth.models import User
# Create your models here.


class IPMarkRemovalRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=12)
    subject_name = models.CharField(max_length=100)
    units = models.IntegerField()
    sem_year = models.CharField(max_length=50)

    instructor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    dean = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name='dean')
    acad = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name='acad')
    registrar = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name='registrar')

    approved_by_faculty = models.BooleanField(default=False)
    approved_by_dean = models.BooleanField(default=False)
    approved_by_ACAD = models.BooleanField(default=False)
    approved_by_registrar = models.BooleanField(default=False)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    date_requested = models.DateTimeField(auto_now_add=True)

    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

    def __str__(self):
            return f"IP Mark Removal Request - {self.student} - {self.subject_code} - {self.subject_name} - {self.units} - {self.sem_year} - {self.date_requested} - {self.status}"
    
class AdditionalFile(models.Model):
      request = models.ForeignKey(IPMarkRemovalRequest, on_delete=models.CASCADE)
      file = models.FileField(upload_to='files/')
      def __str__(self):
            return f"Additional File - {self.request} - {self.file}"
      
class IPMark(models.Model):
    request = models.ForeignKey(IPMarkRemovalRequest, on_delete=models.CASCADE)
    prelim = models.FloatField(null=True, blank=True) 
    midterm = models.FloatField(null=True, blank=True)
    semis = models.FloatField(null=True, blank=True)
    finals = models.FloatField(null=True, blank=True)
    final_grade = models.FloatField(null=True, blank=True) 
    remarks = models.CharField(max_length=10,null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null = True, blank = True)

    
    def __str__(self):
        return f"IP Mark - {self.request.student} - {self.request.subject_code} - Final Grade: {self.final_grade}"