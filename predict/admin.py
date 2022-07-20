from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Predict)
admin.site.register(models.Workload)
