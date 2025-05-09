from django.db import models
from django.contrib.auth.models import User

class Trivia(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)
    image = models.ImageField(upload_to='trivia_images/')
    url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class TriviaScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trivia = models.ForeignKey('Trivia', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    last_played = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.trivia.name} ({self.score})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.score}"