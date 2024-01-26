from django.core.management.base import BaseCommand

from apps.api.models import Vote
from apps.api.csv import Csv


class Command(BaseCommand):
    help = 'Get Users in Forms'

    def add_arguments(self, parser):
        parser.add_argument("form", nargs="+", type=int)

    def handle(self, *args, **options):

        # Get Form ID
        form = options["form"][0]

        # Process CSV
        final_csv = UsersCsv()
        final_csv.process_csv(form)


class UsersCsv:
    def process_csv(self, form, write=True):
        # CSV Headers
        headers = ['ID', 'NOMBRE', 'EMAIL']

        # CSV Rows
        rows = self.build_csv(form)

        # CSV File
        filename = f'form_{form}.csv'

        if write:
            # Create CSV on Disk
            self.write_csv(headers, rows, filename)
        else:
            return headers, rows

    def build_csv(self, form):
        # Create CSV object
        rows = []

        for vote in Vote.objects.filter(form=form).distinct("user"):
            rows.append({
                'ID': vote.user.id,
                'NOMBRE': vote.user.first_name,
                'EMAIL': vote.user.email
            })

        return rows

    def write_csv(self, headers, rows, file):
        # Create CSV in Disk
        Csv.create(headers=headers, rows=rows, file=file)
