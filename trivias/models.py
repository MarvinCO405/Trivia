from django.db import models
from django.contrib.auth.models import User

class Trivia(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)
    image = models.ImageField(upload_to='trivia_images/')

    def __str__(self):
        return self.name
