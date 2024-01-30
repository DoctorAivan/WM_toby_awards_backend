from django.core.management.base import BaseCommand
from django.db.models import F
from apps.api.models import Player


class Command(BaseCommand):
    help = 'Get json players'

    def handle(self, *args, **options):
        player = Player.objects.all().annotate(
            category_name=F('category__name')
        ).values(
            "id", "name", "category_name"
        )
        print(list(player))
