import csv
from django.conf import settings

# Funciones de files CSV
class Csv():
    # Create CSV on disk
    def create(headers, rows, file=None):
        # Configuration
        delimiter = ';'
        encoding = 'utf-8'

        # Define file path
        csv_path = f'{settings.CSV_PATH}/{file}'

        # File instance
        with open(csv_path, 'w', newline = '', encoding = encoding) as csv_file:

            csv_file.write('\ufeff')
            
            writer = csv.DictWriter(
                csv_file,
                fieldnames = headers,
                delimiter = delimiter
            )

            writer.writeheader()
            writer.writerows(rows)

        # Log
        print(f'Create {file} OK')
