from django.core.management.base import BaseCommand, CommandError
import csv
import io
from invoicing.UserMigration import updateCompany
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import os
from django.conf import settings

class Command(BaseCommand):

    help = 'Migrate Company Email Field'

    def handle(self, *args, **options):
        with io.open('compmail.csv','r', encoding='ISO-8859-1') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            error_count = 0
            success_count = 0
            html_errors = ''

            for row in csv_reader:
                instance = updateCompany(
                    {
                    "index": int(row[0]),
                    "email": row[20],
                    "code": row[3].strip()
                    }
                )
        
                print(f"Migrating Email Processed Lines {line_count}")
                line_count += 1

                if instance['status'] == False:
                    print(f"Migrating Email Error Count {error_count}")
                    error_count += 1
                    html_errors += mark_safe(instance['html'])

                else:
                    print(f"Migrating Email Success Count {success_count}")
                    success_count += 1

            csv_file.__exit__()
            f = open(os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates") + '/base_logs_2.html', "w")
            html = render_to_string('base_logs_3.html', {'table_data': mark_safe(html_errors)})
            f.write(html)
            f.close()