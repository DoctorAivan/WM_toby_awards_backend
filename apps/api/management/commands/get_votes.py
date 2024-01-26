from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.api.models import PlayerCategory, Player, Vote
from apps.api.csv import Csv


class Command(BaseCommand):
    help = 'Get Players votes count by Category'

    def handle(self, *args, **options):
        final_csv = VotesCsv()
        final_csv.process_csv()


class VotesCsv:
    def process_csv(self, write=True, form=''):
        # CSV Headers
        headers = ['ID', 'NOMBRE', 'VOTOS', 'PORCENTAJE']

        # CSV Rows
        rows = self.build_csv(form)

        # File name
        filename = f'votos_form_{form}.csv'

        if write:
            # Create CSV on Disk
            self.write_csv(headers, rows, filename)
        else:
            return headers, rows

    def build_csv(self, form):
        # Create CSV object
        rows = []

        rows.append({
            'ID': '',
            'NOMBRE': '',
            'VOTOS': '',
            'PORCENTAJE': ''
        })

        total_votes = 0

        form_id = form

        votes = (
            PlayerCategory.objects.filter(players__votes__form=form_id)
            .annotate(total_votes=Count("players__votes"))
        )

        for category in votes:
            rows.append({
                'ID': '',
                'NOMBRE': category.name.replace('_',' ').upper(),
                'VOTOS': '',
                'PORCENTAJE': ''
            })

            total_votes += category.total_votes

            votes = []

            for player in category.players.all():
                _votes = player.votes.filter(form=form_id)
                if _votes.count():
                    percent = _votes.count() / category.total_votes * 100
                else:
                    percent = 0

                votes.append({
                    'name': player.name,
                    'votes': _votes.count(),
                    'percent': "{:.2f}%".format(percent)
                })

            votes_sorted = sorted(votes, key=lambda x: x['votes'], reverse=True)

            id_list = 1

            # Imprimir el resultado
            for v in votes_sorted:
                rows.append({
                    'ID': id_list,
                    'NOMBRE': v['name'],
                    'VOTOS': v['votes'],
                    'PORCENTAJE': v['percent']
                })

                id_list += 1

            rows.append({
                'ID': '',
                'NOMBRE': '',
                'VOTOS': '',
                'PORCENTAJE': ''
            })

        rows.append({
            'ID': '',
            'NOMBRE': 'VOTOS TOTALES',
            'VOTOS': format(total_votes),
            'PORCENTAJE': ''
        })

        return rows

    def write_csv(self, headers, rows, file):
        # Create CSV in Disk
        Csv.create(headers=headers, rows=rows, file=file)