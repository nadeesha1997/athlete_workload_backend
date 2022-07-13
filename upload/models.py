from django.db import models
from authentication.models import User


# Create your models here.
class Upload(models.Model):
    date = models.DateField()
    data = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_user')


class MergeData(models.Model):
    data = models.JSONField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merge_upload_user')
