from django.db import models
    

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=64)
    image = models.URLField(max_length=64)


class Book(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_page = models.BooleanField()