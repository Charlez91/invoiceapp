from invoicing.models import InvoiceItems
from invoicing.models import SwInvoice
from invoicing.models import SwSearchMasterTbl
from invoicing.models import Company
from invoicing.models import SwProductPricing
from django.db.models import Q
from datetime import datetime , timedelta
from django.conf import settings
import pdfkit
import os
import shutil
from django.template.loader import render_to_string
from django.utils import timezone
import random
import requests
import json
import pytz
class InvoiceGenerator:
    
    def __init__(self, dates, override, *args, **kwargs):
        self.file_path       = os.path.join(os.path.dirname(settings.BASE_DIR), "files")
        self.file_path_1     = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "static")
        self.file_path_2     = os.path.join(os.path.dirname(settings.BASE_DIR), "src")
        self.templates_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates")
        self.products       = {'section66':'SWR66C', 'sewerServiceDiagram' : 'SWRSSD', 'serviceLocationPrint' : 'SWRSLP', 'buildingOverOrAdjacentToSewer' : 'SWRBOA', 'specialMeterReading' : 'SWRSMR', 'section88G' : 'SWR88G'}

        self.dates = dates
        self.override = override

        self.from_date = datetime.strptime(self.dates['sdate'] + ' 13:00:00', "%Y-%m-%d %H:%M:%S")
        self.to_date = datetime.strptime(self.dates['edate'] + ' 13:00:00', "%Y-%m-%d %H:%M:%S")
        
        tz = timezone.get_current_timezone()
        self.from_date = timezone.make_aware(self.from_date, tz, True)
        self.to_date = timezone.make_aware(self.to_date, tz, True)

        new_start_date = self.from_date - timedelta(days=1)

        self.transactions = None

        if self.override:
            new_end_date = self.to_date + timedelta(days=1)
        else:
            new_end_date = self.to_date

        if new_start_date == new_end_date:

            self.transactions = SwSearchMasterTbl.objects.filter(
                date_closed__icontains=self.dates['sdate']
                ).filter(Q(product_status='Closed') | Q(product_status="Completed")).exclude(applicationid = None).exclude(date_closed=None).order_by('-date_closed')

        else:

            self.transactions = SwSearchMasterTbl.objects.filter(
                date_closed__range=(self.from_date,self.to_date)
                ).filter(Q(product_status='Closed') | Q(product_status="Completed")).exclude(applicationid = None).exclude(date_closed=None).order_by('-date_closed')

            print(self.transactions.query)
        
    def generate_invoice_id(self):
        today               = datetime.today()
        today_string        = today.strftime('%y%m%d')
        next_invoice_number = '01'

        last_invoice        = InvoiceItems.objects.all().order_by('invoice_id').last()

        if last_invoice:
            #last_invoice_number = str(last_invoice.invoice_id)[6:]
            last_invoice_number = str(last_invoice.invoice.invoice_id)[6:]
            #num = last_invoice_number + str(1)
            num = int(last_invoice_number) + 1
            next_invoice_number = '{0:02d}'.format(int(num))
        invoice_id = today_string + next_invoice_number

        return invoice_id
        
    def utc_to_sydney(self, d1):
        if d1 == None:
            return None
        try:
            d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
        except TypeError:
            pass
        
        d2 = d1.replace(tzinfo=pytz.UTC)
        d3 = d2.astimezone(pytz.timezone("Australia/Sydney"))
        
        return d3.strftime('%Y-%m-%d')

    def get_invoice_data(self):

        company = []

        for x in self.transactions:

            try:
                user = x.internal_username
            except:
                user = None

            if user != None:
                code = user.split('+')[0]

                if code.upper() not in company:
                    company.append(code.upper())
        f = 0
        invoice_paths = []
        for x in company:
            filtered = self.transactions.filter(internal_username__icontains=x + '+')

            try:
                company_instance = Company.objects.get(compcode=x)
            except:
                company_instance = None

            data = []
            invoice_items = []
            total = 0
            gst_total = 0
            search_charge = 0
            service_charge = 0 
            searches_no = 0
            for y in filtered:
                
                try:
                    product = SwProductPricing.objects.get(product_code=self.products[y.product_name.strip()])
                except:
                    product = None


                try:
                    checker =  InvoiceItems.objects.get(transaction=y.id)
                except Exception as e:
                    checker = None

                if product != None and company_instance != None and checker == None :
                    searches_no = searches_no + 1
                    if product.product_gst_fees == "Yes":
                        gst = 0.1 * product.product_price
                    else:
                        gst = 0.1 * product.sw_product_fees
                    try:
                        username = user.split('+')[1]
                    except:
                        username = "No Username Available"

                    data.append({
                        "username": y.internal_username.split('+')[1], 
                        "date_ordered": self.utc_to_sydney(y.order_datetime),
                        "reference": "Sydney Water Search",
                        "product_code": product.product_code,
                        "client_reference": y.applicantreferencenumber,
                        "disb": product.sw_product_fees,
                        "charge": product.product_price,
                        "disb_charge": product.sw_product_fees + product.product_price,
                        "gst": gst,
                        "disb_charge_gst": (product.sw_product_fees + product.product_price) + gst,
                        "date_closed": y.date_closed.strftime("%Y-%m-%d")
                        })

                    invoice_items.append({
                        "count": searches_no, 
                        "username": y.internal_username.split('+')[1], 
                        "date_ordered": y.order_datetime, 
                        "reference": "Sydney Water Search",
                        "client_reference": y.applicantreferencenumber,
                        "disb": product.sw_product_fees,
                        "charge": product.product_price,
                        "disb_charge": product.sw_product_fees + product.product_price,
                        "gst_amount":  gst,
                        "gst_inc": (product.sw_product_fees + product.product_price) + gst,
                        "transaction": y.id,
                        "date_closed": y.date_closed
                    })

                    search_charge = search_charge + product.sw_product_fees
                    service_charge = service_charge + product.product_price

                    total = total + (product.sw_product_fees + product.product_price) + gst
                    gst_total = gst_total + gst

            if company_instance != None and len(data) > 0:
                try:
                    discount = company_instance.discount.discount
                except:
                    discount = 0
    
                total_disc = total * (discount / 100)
                total_disc = total - total_disc
                date_now = datetime.now().strftime('%B-%d-%Y-%H-%M-%S')

                invoice_id = self.generate_invoice_id()

                context = {
                    "data": data,
                    "date_now": datetime.now().strftime('%B %d, %Y'),
                    "today": date_now,
                    "total": total,
                    "tax": round(gst_total,2),
                    "total_after_discount": round(total_disc,2),
                    "company_discount": discount,
                    "start_date": self.dates['sdate'],
                    "end_date": self.dates['edate'],
                    "invoice_id": invoice_id,
                    "company_instance": company_instance,
                }

                f = f + 1

                rendered = render_to_string('template.html', context)

                file_name_1 = "sample-" + str(f) + ".html"
                file_name_2 = "invoice-" + str(f) + ".pdf"

                try:
                    with open(file_name_1,"w", encoding="utf-8") as html:
                        html.write(rendered)
                        html.close()
                except Exception as e:
                    print(rendered)
                    print(e)

                try:
                    pdfkit.from_file(file_name_1, file_name_2)

                except Exception as e:

                    print(e)

                shutil.copyfile(self.file_path_2 +'/'+ file_name_2, self.file_path_1 + "/files/" + file_name_2)

                new_folder = random.randint(1,3910209312)
                final_folder = '{path}/{folder}'.format(path=self.file_path, folder=new_folder)

                if not os.path.exists(final_folder):
                    os.makedirs(final_folder)

                shutil.move(file_name_2, final_folder)
                
                
                from_date = datetime.strptime(self.dates['sdate'], "%Y-%m-%d")
                to_date = datetime.strptime(self.dates['edate'], "%Y-%m-%d")

                invoice = SwInvoice.objects.create(
                    invoice_id=invoice_id,
                    company_name=company_instance.compname,
                    cmpany_code=company_instance.compcode,
                    searches_from=from_date,
                    searches_to=to_date,
                    search_charge = search_charge,
                    service_charge  = service_charge,
                    gst_charge = gst_total,
                    total_price= total_disc,
                    searches_no= searches_no,
                    pdf_link = final_folder + '/' + file_name_2,
                    payment_status = ''
                )

                invoice_paths.append(self.file_path_1 + "/files/" + file_name_2)

                invoice.save()

                for x in invoice_items:
                    new_items = InvoiceItems.objects.create()
                    for y in x.keys():
                        setattr(new_items,y,x[y])
                        setattr(new_items, 'invoice', invoice)
                        new_items.save()
                
                headers = {
                    'Authorization': 'Bearer CIUi51PTEA4bPR9jksNecoG.6oJPNtkpKMyUf3CG4GTEtnYi',
                    'FROM_ADMIN': 'Yes',
                    'Content-type': 'application/json'
                }
                
                email = ''
                if company_instance.compemail1 == None or company_instance.compemail1 == '' or company_instance.compemail1 == 'None':

                    email = 'support.rubela.shome@gmail.com'

                else:
                    email = company_instance.compemail1
                
                dataemail = {}
                if int(settings.REAL_EMAIL) == 1:
                    dataemail = {"id": invoice.id, "file_name": file_name_2, "comp_mail": email}
                else:
                    dataemail = {"id": invoice.id, "file_name": file_name_2, "comp_mail": settings.DEMO_EMAIL}
                if str(settings.DEV).lower() == 'no':
                    response = requests.post(url=f"{settings.API_URL}/invoice/email",data=json.dumps(dataemail), stream=True,headers=headers)

        return invoice_paths