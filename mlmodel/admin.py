from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.MlModel)
admin.site.register(models.ModelSport)
admin.site.register(models.TrainData)