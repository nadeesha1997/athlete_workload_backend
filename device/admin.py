from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.MountPlace)
admin.site.register(models.Device)
admin.site.register(models.Reading)
admin.site.register(models.SportMountPlace)
