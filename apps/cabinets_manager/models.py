from django.db import models
from apps.cabinets.models import Cabinets
from apps.users.models import Users

class CabinetsManager(models.Model):
    cabinet_id = models.OneToOneField(Cabinets, on_delete=models.CASCADE)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    initial_datetime = models.DateTimeField(auto_now_add=True)
    final_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.cabinet_id) + str(self.owner)
    
class CabinetsManagerHistory(models.Model):
    cabinet_id = models.ForeignKey(Cabinets, on_delete=models.CASCADE, unique=False, editable=False)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, unique=False, editable=False)
    initial_datetime = models.DateTimeField(editable=False)
    final_datetime = models.DateTimeField(editable=False)

    def __str__(self):
        return str(self.cabinet_id) + str(self.owner)

class EmployeeExit(models.Model):
    cabinet = models.OneToOneField(Cabinets, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.cabinet+"@"+self.user

class EmployeeExitHistory(models.Model):
    cabinet = models.ForeignKey(Cabinets, on_delete=models.CASCADE, editable=False, unique=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, editable=False, unique=False)
    authorized = models.BooleanField( editable=False, unique=False)

    def __str__(self):
        return str(self.cabinet)+"@"+str(self.user)
    
class History(models.Model):
    cabinet = models.ForeignKey(Cabinets, on_delete=models.CASCADE, editable=False, unique=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, editable=False, unique=False)
    authorized = models.BooleanField( editable=False, unique=False)
    initial_datetime = models.DateTimeField(editable=False)
    final_datetime = models.DateTimeField(editable=False)

    def __str__(self):
        return str(self.cabinet)+"@"+str(self.user)