from invoicing.models import InvoiceItems
from invoicing.models import SwInvoice
from invoicing.models import SwSearchMasterTbl
from invoicing.models import Company
from datetime import datetime , timedelta
from django.conf import settings
from django.utils import timezone
import pdfkit
import os
import shutil
from django.template.loader import render_to_string


class Invoice:
    
    def __init__(self, *args, **kwargs):
        self.files_path = os.path.join(os.path.dirname(settings.BASE_DIR), "files")
        self.static_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "static")
        self.src_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src")
        self.templates_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates")

    def update(self, *args, **kwargs):
        
        try:
            kwargs.get('id')
        except Exception as e:
            raise e

        invoice_items = InvoiceItems.objects.filter(invoice=kwargs.get('id')).order_by('-date_ordered')
        start_date = InvoiceItems.objects.filter(invoice=kwargs.get('id')).exclude(transaction__isnull=True).order_by('date_ordered').first()
        end_date = InvoiceItems.objects.filter(invoice=kwargs.get('id')).exclude(transaction__isnull=True).order_by('-date_ordered').first()

        company_code = SwSearchMasterTbl.objects.get(id=end_date.transaction)
        company_code = company_code.internal_username.split('+')[0]
        company_instance = Company.objects.get(compcode=company_code)


        invoice_instance = SwInvoice.objects.get(id=kwargs.get('id'))
        invoice_from_date = invoice_instance.searches_from
        invoice_to_date = invoice_instance.searches_to

        total = 0
        gst_total = 0
        disb_total = 0
        charge_total = 0
        for x in invoice_items:
            total = total + x.gst_inc
            gst_total = gst_total + x.gst_amount
            disb_total = disb_total + x.disb
            charge_total = charge_total + x.charge
        try:
            cpdiscount = company_instance.discount.discount
            total_disc = total * (cpdiscount / 100)
        except Exception:
            cpdiscount = 0
            total_disc = total * (0 / 100)
        total_disc = total - total_disc
        date_now = datetime.now().strftime('%B-%d-%Y-%H-%M-%S')
        context = {
            "invoices": invoice_items,
            "start_date": invoice_from_date,
            "end_date": invoice_to_date,
            "company_instance": company_instance,
            "invoice_instance": invoice_instance,
            "date_now": datetime.now().strftime('%B %d, %Y'),
            "total": round(total,2),
            "company_discount": cpdiscount,
            "total_after_discount": round(total_disc,2),
            "tax": round(gst_total,2),
            "real_total": round(total_disc,2)

        }
       
        rendered = render_to_string('invoice_template.html', context)

        with open('update-1.html',"w") as html:
            html.write(rendered)
            html.close()
        file_name = 'invoice-' + date_now + '.pdf'
        pdfkit.from_file('update-1.html', file_name)
        
        # Done to allow path split in windows also
        try:
            paths = invoice_instance.pdf_link.path.split("/")
            files_folder = paths[-2]
        except:
            paths = invoice_instance.pdf_link.path.split("\\")

        final_folder = self.files_path + '/' + paths[-2] + "/"
        shutil.move(file_name, final_folder)

        invoice_instance.pdf_link = final_folder + file_name
        invoice_instance.search_charge = disb_total
        invoice_instance.service_charge = charge_total
        invoice_instance.gst_charge = gst_total
        invoice_instance.total_price = round(total_disc,2)
        invoice_instance.save()

        return invoice_instance

