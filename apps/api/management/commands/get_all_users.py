from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.api.models import Vote
from apps.api.csv import Csv


class Command(BaseCommand):
    help = 'Get Users in Forms'

    def handle(self, *args, **options):
        final_csv = AllUsersCsv()
        final_csv.process_csv()


class AllUsersCsv:
    def process_csv(self, write=True):

        # CSV Headers
        headers = ['ID', 'NOMBRE', 'EMAIL']

        # CSV Rows
        rows = self.build_csv()

        # File name
        filename = f'usuarios.csv'

        if write:
            # Create CSV on Disk
            self.write_csv(headers, rows, filename)
        else:
            return headers, rows

    def build_csv(self):
        # Create CSV object
        rows = []

        for user in User.objects.all():
            rows.append({
                'ID': user.id,
                'NOMBRE': user.first_name,
                'EMAIL': user.email
            })

        return rows

    def write_csv(self, headers, rows, file):
        # Create CSV on Disk
        Csv.create(headers=headers, rows=rows, file=file)