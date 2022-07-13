from django.db import models

from sport.models import Sport

# Create your models here.
class MlModel(models.Model):
    model_name=models.CharField(max_length=50)
    model_file=models.FileField(upload_to='ml')

class TrainData(models.Model):
    data_set=models.JSONField()
    sport=models.ForeignKey(Sport,related_name='train_sport',on_delete=models.CASCADE)

class ModelSport(models.Model):
    sport=models.ForeignKey(Sport,related_name='sport',on_delete=models.CASCADE)
    first_model=models.ForeignKey(MlModel,related_name='main_model',on_delete=models.CASCADE)
    second_model=models.ForeignKey(MlModel,related_name='alternate_model',on_delete=models.CASCADE)