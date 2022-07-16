import datetime

from django.db import models

from authentication.models import User
from mlmodel.models import MlModel

# Create your models here.
from upload.models import MergeData


class Predict(models.Model):
    ml_model = models.ForeignKey(MlModel, related_name="ml_model", on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today())
    dataset = models.ForeignKey(MergeData, on_delete=models.CASCADE, related_name="dataset")

    def __str__(self):
        return f"<{self.date}>"


class Workload(models.Model):
    workload_data = models.JSONField()
    date = models.DateField(default=datetime.date.today())
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='predict_date')

    def __str__(self):
        return f"<{self.date}>"
