from django.db import models

# Create your models here.
class MlModel(models.Model):
    model_name=models.CharField(max_length=50)
    model_file=models.FileField(upload_to='ml')

class TrainData(models.Model):
    data_set=models.JSONField()