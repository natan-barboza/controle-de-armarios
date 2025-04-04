from django.db import models

class Cabinets(models.Model):
    cabinet = models.IntegerField()
    status = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cabinet)