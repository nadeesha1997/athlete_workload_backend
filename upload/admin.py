from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Upload)
admin.site.register(models.MergeData)
