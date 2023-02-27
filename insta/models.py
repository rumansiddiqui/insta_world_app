from django.db import models


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=500)
    photo = models.ImageField(upload_to="img/")


class Post(models.Model):
    image = models.ImageField(upload_to="img/")
    description = models.CharField(max_length=200)
