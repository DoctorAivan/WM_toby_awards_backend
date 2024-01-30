from django.core.management.base import BaseCommand
from apps.api.data.player_list import categories, players
from apps.api.models import Player, PlayerCategory


class Command(BaseCommand):
    help = 'Load data from fixture'

    def handle(self, *args, **options):
        # Load categories
        for category in categories:
            PlayerCategory.objects.get_or_create(name=category)
            self.stdout.write(self.style.SUCCESS(f'Category {category} loaded successfully'))

        # Load players
        for category, player_list in players.items():
            category = PlayerCategory.objects.get(name=category)
            for player in player_list:

                Player.objects.get_or_create(
                    name=player,
                    category=category
                )
                self.stdout.write(self.style.SUCCESS(f'Player {player} loaded successfully'))
