from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'
