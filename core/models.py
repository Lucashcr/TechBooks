from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=256)
    is_page = models.BooleanField(default=True)
    
