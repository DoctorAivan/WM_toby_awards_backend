from django.db import models


class PlayerCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(PlayerCategory, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return self.name


class Vote(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='votes')
    form = models.SmallIntegerField()
