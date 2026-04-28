from django.db import models
from django.contrib.auth.models import User

class StudentRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_records')
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    year_level = models.IntegerField()
    
    def __str__(self):
        return f"{self.full_name} - {self.course} (Year {self.year_level})"
    