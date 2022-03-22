from django.core.management.base import BaseCommand, CommandError
import csv
import io
from invoicing.UserMigration import migrate, insertEmail, emailmigrate
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import os
from django.conf import settings

class Command(BaseCommand):

    help = 'Migrate User Email Field'

    def handle(self, *args, **options):
        with io.open('newCsv.csv','r', encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            error_count = 0
            success_count = 0
            html_errors = ''

            for row in csv_reader:
                instance = emailmigrate(
                    {
                    "username": f"{row[2]}+{row[1]}",
                    "id": row[5]
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
            print(os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates"))
            f = open(os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates") + '/base_logs_1.html', "w")
            html = render_to_string('base_logs.html', {'table_data': mark_safe(html_errors)})
            f.write(html)
            f.close()

        with io.open('useremail.csv','r', encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            error_count = 0
            success_count = 0
            html_errors = ''

            for row in csv_reader:
                instance = insertEmail(
                    {
                    "email": row[10],
                    "id": row[1],
                    'fname': row[3],
                    "lname": row[4],
                    "title": row[2]
                    }
                )
        
                print(f"Inserting Email Lines {line_count}")
                line_count += 1

                if instance['status'] == False:
                    print(f"Inserting Email Error Count {error_count}")
                    error_count += 1
                    html_errors += mark_safe(instance['html'])

                else:
                    print(f"Inserting Email Success Count {success_count}")
                    success_count += 1

            csv_file.__exit__()
            print(os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates"))
            f = open(os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates") + '/base_logs_1.html', "w")
            html = render_to_string('base_logs.html', {'table_data': mark_safe(html_errors)})
            f.write(html)
            f.close()