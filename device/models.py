from django.db import models

# Create your models here.
class MountPlace(models.Model):
    place=models.CharField()

class Device(models.Model):
    device_id=models.CharField()
    mount=models.ForeignKey(MountPlace,related_name='place',on_delete=models.CASCADE)

class Reading(models.Model):
    device=models.ForeignKey(Device,related_name='device',on_delete=models.CASCADE)
    value=models.FloatField()