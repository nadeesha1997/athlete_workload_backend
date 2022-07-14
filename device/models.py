from django.db import models

# Create your models here.
from sport.models import Sport


class MountPlace(models.Model):
    place = models.CharField(max_length=50)

    def __str__(self):
        return self.place


class Device(models.Model):
    device_id = models.CharField(max_length=5)
    mount = models.ForeignKey(MountPlace, related_name='mount_place', on_delete=models.CASCADE)

    def __str__(self):
        return f"<{self.device_id}-{self.mount}>"


class Reading(models.Model):
    device = models.ForeignKey(Device, related_name='related_device', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"<{self.value} - {self.device}>"


class SportMountPlace(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='sport_sportmount')
    place = models.ForeignKey(MountPlace, on_delete=models.CASCADE, related_name='place_sportmount')

    def __str__(self):
        return f"<{self.sport}-{self.place}>"
