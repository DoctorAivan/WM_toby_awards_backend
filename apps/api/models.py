from django.db import models


class PlayerCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=64)
    team = models.CharField(max_length=64, null=True, blank=True)
    category = models.ForeignKey(PlayerCategory, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return self.name


class Vote(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='votes')
    form = models.SmallIntegerField()
