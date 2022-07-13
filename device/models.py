from django.db import models

# Create your models here.
class MountPlace(models.Model):
    place=models.CharField(max_length=50)

class Device(models.Model):
    device_id=models.CharField(max_length=5)
    mount=models.ForeignKey(MountPlace,related_name='mount_place',on_delete=models.CASCADE)

class Reading(models.Model):
    device=models.ForeignKey(Device,related_name='related_device',on_delete=models.CASCADE)
    value=models.FloatField()