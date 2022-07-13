from django.db import models

from mlmodel.models import MlModel

# Create your models here.
class Predict(models.Model):
    ml_model=models.ForeignKey(MlModel,related_name="ml_model",on_delete=models.CASCADE)
    date=models.DateField()