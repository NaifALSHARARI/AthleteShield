from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    minutes_played = models.FloatField(default=0.0)
    training_load = models.FloatField(default=0.0)
    prev_injuries = models.IntegerField(default=0)
    age = models.IntegerField(default=20)

    def __str__(self):
        return self.name
