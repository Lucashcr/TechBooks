from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    subject = models.CharField(max_length=64)
    is_page = models.BooleanField()
    
