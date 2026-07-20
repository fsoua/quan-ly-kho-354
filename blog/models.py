from django.db import models
class Tasks(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateField()
    comleted = models.BooleanField()
    created_date = models.DateField(auto_now_add=True)
# Create your models here.
