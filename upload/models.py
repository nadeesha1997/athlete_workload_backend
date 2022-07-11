from django.db import models

# Create your models here.
class Upload(models.Model):
    date=models.DateField()
    data=models.JSONField()
