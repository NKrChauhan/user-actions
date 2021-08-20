from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Task(models.Model):
    initiated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='initiated_by')
    assigned_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_by')
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_to')
    completed = models.BooleanField(default=True)
    
