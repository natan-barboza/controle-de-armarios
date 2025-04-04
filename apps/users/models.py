from django.db import models

# Create your models here.

class Users(models.Model):
    full_name = models.CharField(max_length=100)
    enterprise_id = models.CharField(max_length=10, unique=True)
    status = models.BooleanField()
    personal_id = models.CharField(max_length=14, unique=True)

    def __str__(self) -> str:
        return f"{self.enterprise_id}@{self.full_name}"
