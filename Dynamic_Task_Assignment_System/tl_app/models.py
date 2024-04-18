from django.db import models

from accounts.models import *

# Create your models here.
class Task(BaseModel):
    STATUS_CHOICES = [
        ('TO_DO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'LOW'),
        ('HIGH', 'HIGH'),
        ('CRITICAL', 'CRITICAL'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='tasks')
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    deadline = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TO_DO')
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='LOW')