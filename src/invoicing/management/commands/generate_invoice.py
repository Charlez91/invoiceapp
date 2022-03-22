from django.core.management.base import BaseCommand, CommandError
import os

from django.conf import settings
from datetime import datetime
import datetime as DT
from invoicing.models import SwSearchMasterTbl,  HazCustomerMasterTbl, Company, SwProductPricing, SwInvoice
from invoicing.ingen import InvoiceGenerator
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-s", "--start", type=str)
        parser.add_argument("-e", "--end", type=str)

    def handle(self, *args, **options):
        today = options["start"] if options["start"] else None
        
        end = options["end"] if options["end"] else None

        override = False

        if end != None or today != None:
            override = True
        else:
            override = False

        try:
            if today == None:
                today = datetime.today() - DT.timedelta(days=7)
                today.strftime('%Y-%m-%d')
            else:
                today = datetime.strptime(today, ('%Y-%m-%d'))
        except:
            raise ValueError("Start date format should be YYYY-mm-dd")

        try:
            if end == None:
                end = datetime.today().strftime('%Y-%m-%d')
            end = datetime.strptime(end, ('%Y-%m-%d'))
        except:
            raise ValueError("End date format should be YYYY-mm-dd")

        print(f"Starting Invoice Generator Start Date: {today} & End Date: {end}")

        data = {'sdate': today.strftime('%Y-%m-%d'), 'edate': end.strftime('%Y-%m-%d')}
        rary = InvoiceGenerator(data, override)
        result = rary.get_invoice_data()

        if result != "": 
            data["success"] = "Invoice Generated"
            data["code"]    = "true"
            data["paths"]   = result
        else:
            data['code'] = 'false'
            data["error"] = "No matching data on the database"
        
        f = open(os.path.join(os.path.dirname(settings.BASE_DIR), "src") + '\\invoice_logs.json', "a")
        f.write(str(data))
        f.close()

        print(data)
