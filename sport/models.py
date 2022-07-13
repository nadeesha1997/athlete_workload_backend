from django.db import models

# Create your models here.
class Sport(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return f"<sport : {self.name}>"

class Activity(models.Model):
    id_field=models.IntegerField()
    name=models.CharField(max_length=50)
    sport=models.ForeignKey(Sport,related_name='Sport',on_delete=models.CASCADE)

    def __str__(self):
        return f"<{self.id_field} : {self.name} : {self.sport}>"
