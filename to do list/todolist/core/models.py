from django.db import models
from django.contrib.auth.models import User
class TaskList(models.Model):
    TASK_TYPE_CHOICES = [
        ('work', 'Work'),
        ('urgent', 'Urgent'),
        ('personal', 'Personal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate task with user
    task = models.TextField()
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES, default='work')
    task_time = models.DateTimeField(default="1900-01-01 00:00:00") 
    def __str__(self):
        return self.task

