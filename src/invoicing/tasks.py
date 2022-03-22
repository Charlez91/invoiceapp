from __future__ import absolute_import, unicode_literals    
from celery import shared_task 
from .models import SwSearchMasterTbl,HazCustomerMasterTbl, SwInvoice, AuthUser, DiscountTbl, InvoiceItems
from configparser import ConfigParser
from celery import shared_task   
from datetime import datetime , timedelta
from django.utils import timezone
from django.conf import settings
import datetime as DT
import pdfkit
import shutil
import random
import os
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
import requests
import json
from django.conf import settings
# from weasyprint import HTML
# from pdf import PDFgenerator   
  
# @shared_task 
class InvoiceGenerator:

    # Init Method for invoice generator class
    def __init__(self, MasterTbl, UserTbl, CompanyTbl, ProductPricing, InvoiceTbl,dates, override):
        """
            Function to initialize Invoice Generator Class
            set all model, array and dict fiels
            parameter 1     : Master Table Object
            parameter 2     : Customer Table Object
            parameter 3     : Comapny Table Object
            parameter 4     : Product Pricing Table Object 
            parameter 5     : Invoice Table Object   
        """
        self.invoice        = []
        self.done_user      = [] 
        self.master_tbl     = MasterTbl
        self.users          = UserTbl
        self.companys       = CompanyTbl
        self.invoiceT       = InvoiceTbl
        self.productP       = ProductPricing
        self.file_path       = os.path.join(os.path.dirname(settings.BASE_DIR), "files")
        self.file_path_1     = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "static")
        self.file_path_2     = os.path.join(os.path.dirname(settings.BASE_DIR), "src")
        self.products       = {'section66':'SWR66C', 'sewerServiceDiagram' : 'SWRSSD', 'serviceLocationPrint' : 'SWRSLP', 'buildingOverOrAdjacentToSewer' : 'SWRBOA', 'specialMeterReading' : 'SWRSMR', 'section88G' : 'SWR88G'}
        self.dates = dates
        self.override = override
    # Method to get search date from and to
    def setTransactionDate(self):

        self.from_date      = datetime.strptime(self.dates['sdate'] + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
        self.to_date        = datetime.strptime(self.dates['edate'] + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
        tz                  = timezone.get_current_timezone()
        
        self.transactions = None
        if (self.from_date is not None and self.from_date != "") and (self.to_date is not None and self.to_date != ""):
            self.from_date           = timezone.make_aware(self.from_date, tz, True)
            self.to_date             = timezone.make_aware(self.to_date, tz, True)

            new_start_date = self.from_date - timedelta(days=1)
            if self.override:
                new_end_date = self.to_date + timedelta(days=1)
            else:
                new_end_date = self.to_date

            if new_start_date == new_end_date:
                self.transactions   = self.master_tbl.objects.filter(order_datetime__icontains=self.dates['sdate']).exclude(applicationid = None).order_by('-order_datetime')
            else:
                self.transactions   = self.master_tbl.objects.filter(order_datetime__range=(new_start_date,new_end_date)).exclude(applicationid = None).order_by('-order_datetime')
                
    # Method to generate unique invoice id
    def generate_invoice_id(self):
        """
            Function to generate a unique invoice ID based on 
            current date and the last id in the table
            returns invoice id
            
        """
        today               = datetime.today()
        today_string        = today.strftime('%y%m%d')
        next_invoice_number = '01'
        last_invoice        = self.invoiceT.objects.filter(invoice_id__startswith=today_string).order_by('invoice_id').last()
        if last_invoice:
            last_invoice_number = int(last_invoice.invoice_id[6:])
            next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)
        invoice_id = today_string + next_invoice_number
        return invoice_id

    # Method to get invoice data fromdatabase and store in invoice array
    def get_invoice_data(self):
        """
            Function to extract invoice data from the models and store
            in an invoice array for every user
            returns invoice array
            
        """
        today                   = datetime.today()
        i                       = 0
        gst                     = 0

        for a in self.transactions:
            try:
                us = AuthUser.objects.get(username=a.internal_username)
            except:
                us = None
            
            username = a.internal_username
            real_username = ''
            if username is not None:
                code = username.split("+")
                try:
                    real_username = code[1]
                except:
                    real_username = username
                try:
                    comp = self.companys.objects.get(compcode=code[0])
                except:
                    comp = None
            else:
                comp = None

            try:
                idy     = a.product_name.strip()
                prd     = self.productP.objects.get(product_code=self.products[idy])
            except:
                prd = None

            
            
            if us != None and comp != None and prd != None:
            #if us != None and prd != None:
                
                if us.first_name in self.done_user:
                    index           = self.done_user.index(us.first_name)
                    realindex       = index + 1
                    realindex       = self.done_user[realindex]

                    rary            = self.invoice[realindex]
                    exist           = rary[len(rary) - 1]
 
                    data    = {}
        
                    try:
                        data['discount']                = comp.discount.discount
                    except:
                        data['discount']                = 0

                    data['real_username']               = real_username
                    try:
                        data["company_name"]            = comp.compname
                    except:
                        data["company_name"]            = "No Company Name Found"
                    try:
                        data["cmpany_code"]             = comp.compcode
                    except:
                        data["cmpany_code"]             = "No Company Code Found"

                    data["cutomer_name"]                = us.first_name
                    
                    data["cutomer_name"]                = us.first_name
                    
                    data['comp_street']             = comp.compstreet if comp.compstreet != None else ' '
                    
                    data['comp_suburb']             = comp.compsuburb if comp.compsuburb != None else ' '
                    
                    data['comp_state']              = comp.compstate if comp.compstate != None else  ' '
                    
                    data['comp_postcode']           = comp.comppostcode if comp.comppostcode != None else ' '

                    data["company_address"]         = data.get("comp_street", ' ') + " " + data.get("comp_suburb", ' ') + " " + data.get("comp_state", ' ') + " " + data.get("comp_postcode", ' ')
                    
                    if data["company_address"].replace(' ','') == '':
                        data['company_address'] = "Company Address Not Available"

                    try:
                        data["phone"]                   = comp.compphone1
                    except:
                        data["phone"]                   = "No Phone Found"
                    try:
                        data["fax"]                     = comp.directfaxnumber
                    except:
                        data["fax"]                     = "No fax Found"

                    try:
                        data['compemail1']              = comp.compemail1
                    except:
                        data['compemail1']              = 'support.rubela.shome@gmail.com'

                    data["Searches_From"]               = self.from_date.strftime('%d/%m/%y')
                    data["Searches_To"]                 = self.to_date.strftime('%d/%m/%y')
                    data["Searches_No"]                 = a.haz_order_id
                    data["trans_id"]                    = a.id
                    data["Search_Charge"]               = prd.sw_product_fees
                    data["Service_Charge"]              = prd.product_price
                    data["date_ordered"]                = a.order_datetime.strftime('%d/%m/%y')
                    data["reference"]                   = "Sydney Water Search"
                    try:
                        if a.applicantreferencenumber is not None:
                            data["client_reference"]           = a.applicantreferencenumber
                        else:
                            data["client_reference"]           = ""
                    except:
                        data["client_reference"]           = ""
                    data["disb"]                        = prd.sw_product_fees
                    data["charge"]                      = prd.product_price
                    data["disb_charge"]                 = prd.sw_product_fees + prd.product_price
                    data["disb_total"]                  = exist["disb_total"] + prd.sw_product_fees
                    data["charge_total"]                = exist["charge_total"] + prd.product_price
                    
                    # invoice number
                    data["last_payment_date"]           = ""
                    data["current_account_balance"]     = ""

                    if prd.product_gst_fees == "Yes":
                        gst      = 0.1 *  prd.product_price
                    else :
                        gst     = 0.1 * prd.sw_product_fees
                    data["GST_Charge"]                  = gst
                    data["disb_charge_total"]           = prd.sw_product_fees + prd.product_price + gst
                    data["total_price"]                 = prd.sw_product_fees + prd.product_price
                    data["disy"]                        = exist["disy"]  + prd.sw_product_fees + prd.product_price
                    data["GST_total"]                   = exist["GST_total"] + gst
                    data["disb_charge_totaly"]          = exist["disb_charge_totaly"] + prd.sw_product_fees + prd.product_price + gst
                    
                    
                    rary.append(data)
                    self.invoice[realindex] = rary

                else:    
                    self.done_user.append(us.first_name)
                    self.done_user.append(i) 
                    usey                    = []
                    data                    = {}

                    try:
                        data['discount']                = comp.discount.discount
                    except:
                        data['discount']                = 0
                    data["invoice_id"]                  = self.generate_invoice_id()
                    try:
                        data["company_name"]            = comp.compname
                    except:
                        data["company_name"]            = "No Company Name Found"
                    try:
                        data["cmpany_code"]             = comp.compcode
                    except:
                        data["cmpany_code"]             = "No Company Code Found"

                    data["cutomer_name"]                = us.first_name

                    data["cutomer_name"]                = us.first_name
                    
                    data['comp_street']             = comp.compstreet if comp.compstreet != None else ' '
                    
                    data['comp_suburb']             = comp.compsuburb if comp.compsuburb != None else ' '
                    
                    data['comp_state']              = comp.compstate if comp.compstate != None else  ' '
                    
                    data['comp_postcode']           = comp.comppostcode if comp.comppostcode != None else ' '

                    data["company_address"]         = data.get("comp_street", ' ') + " " + data.get("comp_suburb", ' ') + " " + data.get("comp_state", ' ') + " " + data.get("comp_postcode", ' ')

                    if data["company_address"].replace(' ','') == '':
                        data['company_address'] = "Company Address Not Available"
                        
                    try:
                        data["phone"]                   = comp.compphone1
                    except:
                        data["phone"]                   = "No Phone Found"
                    try:
                        data["fax"]                     = comp.directfaxnumber
                    except:
                        data["fax"]                     = "No fax Found"

                    try:
                        data['compemail1']              = comp.compemail1
                    except:
                        data['compemail1']              = 'support.rubela.shome@gmail.com'

                    data["Searches_From"]               = self.from_date.strftime('%d/%m/%y')
                    data["Searches_To"]                 = self.to_date.strftime('%d/%m/%y')
                    data["Searches_No"]                 = a.haz_order_id
                    data["trans_id"]                    = a.id
                    data["Search_Charge"]               = prd.sw_product_fees
                    data["Service_Charge"]              = prd.product_price
                    data["date_ordered"]                = a.order_datetime.strftime('%d/%m/%y')
                    data["reference"]                   = "Sydney Water Search"
                    try:
                        if a.applicantreferencenumber is not None:
                            data["client_reference"]           = a.applicantreferencenumber
                        else:
                            data["client_reference"]           = ""
                    except:
                        data["client_reference"]           = ""
                    data["disb"]                        = prd.sw_product_fees
                    data["charge"]                      = prd.product_price
                    data["disb_charge"]                 = prd.sw_product_fees + prd.product_price
                    data["disb_total"]                  = prd.sw_product_fees
                    data["charge_total"]                = prd.product_price
                    data['real_username']               = real_username

                    if prd.product_gst_fees == "Yes":
                        gst      = 0.1 *  prd.product_price
                    else :
                        gst     = 0.1 * prd.sw_product_fees
                    data["GST_Charge"]                  = gst
                    data["disb_charge_total"]           = prd.sw_product_fees + prd.product_price + gst
                    data["total_price"]                 = prd.sw_product_fees + prd.product_price
                    data["GST_total"]                   = gst
                    data["disy"]                        = prd.sw_product_fees + prd.product_price
                    data["disb_charge_totaly"]          = prd.sw_product_fees + prd.product_price + gst
                     # invoice number
                    data["last_payment_date"]           = ""
                    data["current_account_balance"]     = ""

                    # print(data["disb_charge_total"])
                    usey.append(data)
                    self.invoice.append(usey)
                    i +=1
                
            else:
                continue
        
    
        return self.invoice

    # Method to generate pdf file and store in database from invoice array
    def invoice_generator(self, invoice_array, file_path):
        """
            Function to render a pdf file and save data in invoice datatbase
            parameter 1 : invoice array generated
            parameter 2 : path to create and store pdf file
            
        """ 
        today       = datetime.today()
        t           = 0
        gst_total   = 0
        invoice_paths = []
        
        

        html_head   = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>TAX INVOICE</title><link rel="icon" href="/images/favicon.png" type="image/x-icon">
                        <style>body {font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;text-align: center;color: #777;margin: 0;padding: 0;}
                        body .wrapper {position: absolute;top: 0;left: 0;right: 0;max-width: 100%;height: 100%;margin: 0 auto;padding: 20px 30px;}
                        body .wrapper .top {display: inline;width: 100%;}
                        .top h3 {font-weight: 300;margin-top: 10px;margin-bottom: 20px;font-style: italic;color: rgb(48, 36, 100);float: left;}
                        .top h4 {font-weight: 300;margin-top: 10px;margin-bottom: 20px;font-style: italic;color: rgb(48, 36, 100);float: right;}
                        body a {color: #06F;}
                        .invoice-box {margin: 90px auto 20px auto;max-width: 1200px;padding: 20px;border: 1px solid #eee;box-shadow: 0 0 10px rgba(0, 0, 0, .15);font-size: 14px;line-height: 18px;font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;color: #555;height: auto;}
                        .invoice-box .invoice-box-top .container {display: table;height: 100%;width: 100%;}
                        .invoice-box .invoice-box-top {display: table;height: 100%;width: 100%;}
                        .invoice-box .invoice-box-top .col-lft-6 {display: table-cell;text-align: left;vertical-align: middle;width: 50%;padding: 1rem;}
                        .invoice-box .invoice-box-top .col-rght-6 {display: table-cell;text-align: right;vertical-align: middle;width: 50%;}
                        .invoice-box table {width: 100%;font-family: Arial, Helvetica, sans-serif;border-collapse: collapse;}
                        .invoice-box table td, .invoice-box table th {border: 1px solid #ddd;padding: 8px;}
                        .invoice-box table td {padding: 5px;vertical-align: top;color: #000;}
                        .invoice-box table td strong{font-weight: 600;}
                        .invoice-box table tr:nth-child(even){background-color: #f2f2f2}
                        .invoice-box table  tr:hover {background-color: #ddd;}
                        .invoice-box table th {padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #4CAF50;color: white;}
                        .invoice-box .total-summary {/* float: right; */text-align: right;}
                        .invoice-box .total-footer {/* float: right; */text-align: left;}
                        .invoice-box .abf-card {border: 5px solid #0e290f;padding: 20px;box-shadow: 0 10px 10px rgba(0, 0, 0, .15);border-radius: 10px;text-align: left;margin: 10px auto;}
                        .invoice-footer {text-align: center;line-height: 16px;margin: 30px auto;}
                        </style></head>"""
        html_1      = "<body><div class='wrapper'><div class='top'><h3>TAX INVOICE</h3><h4>Froms " + self.from_date.strftime('%d/%m/%y') + " to " + self.to_date.strftime('%d/%m/%y') + "</h3></div>"
        html_2      = ""

        f = 1
        invoice_items = []
        for invs in invoice_array:
            table       = self.invoiceT()
            # print(len(invs))
            file_name_1     = "sample-" + str(f) + ".html"
            file_name_2     = "invoice-" + str(f) + ".pdf"

            t = 1
            gst_total = 0
            html_2 = ''
            disy_total = 0
            disb_total = 0
            charge_total = 0
            invoice_id = self.generate_invoice_id()
            disb_charge_total = 0
            invoice_items = []
            for inv in invs:
                date_from       = datetime.strptime(inv["Searches_From"], "%d/%m/%y")
                date_to         = datetime.strptime(inv["Searches_To"], "%d/%m/%y")
                date_from       = datetime.strftime(date_from, "%Y-%m-%d")
                date_to         = datetime.strftime(date_to, "%Y-%m-%d")
            #save to database First
                table.invoice_id      = invoice_id
                table.company_name    = inv["company_name"]
                table.cmpany_code     = inv["cmpany_code"]
                table.searches_from   = date_from
                table.searches_to     = date_to
                

                gst_total   += inv["GST_Charge"]
                disy_total += inv["disy"]
                disb_total += inv["disb"]
                charge_total += inv["charge"]
                disb_charge_total += inv["disb_charge_total"]
                
                in_items = {
                    "count": t, 
                    "username": inv["real_username"], 
                    "date_ordered": datetime.strptime(inv["date_ordered"], "%d/%m/%y"), 
                    "reference": inv["reference"],
                    "client_reference": inv["client_reference"],
                    "disb": round(inv["disb"],2),
                    "charge": round(inv["charge"],2),
                    "disb_charge": round(inv["disb_charge"],2),
                    "gst_amount":  round(inv["GST_Charge"],2),
                    "gst_inc": round(inv["disb_charge_total"],2),
                    "transaction": inv["trans_id"]
                    }

                invoice_items.append(in_items)

                html_2 += "<tr><th scope='row'>" + str(t) + "</th><td>"+inv["real_username"]+"</td><td>"  +  inv["date_ordered"] + "</td><td>" + inv["reference"] + "</td><td>" + inv["client_reference"]  + "</td><td>" + str(round(inv["disb"],2)) + "</td><td>" + str(round(inv["charge"],2)) + "</td><td>" + str(round(inv["disb_charge"],2)) + "</td><td>" + str(round(inv["GST_Charge"],2))  + "</td><td>" + str(round(inv["disb_charge_total"],2))  + "</td>" 
                t += 1
            table.search_charge   = disb_total
            table.service_charge  = charge_total
            table.gst_charge      = gst_total
            table.searches_no     = t - 1
            table.total_price     = round((float(disb_charge_total) - float(disb_charge_total * inv["discount"]/100)), 2)
        
            logo = """
            data:image/png;base64,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
            """
            html_3   = f"<div class='invoice-box'><div class=''><div class='col-rght-12' ><img style='max-width: 215px;' src='{logo}'></div><div class='invoice-box-top'><div class='col-lft-6'>" + "<h4>Account Name : " + inv.get("company_name", "No Company Name Found") + " </h4>""<h4>Address : " + inv.get("company_address", "No Address Found") + "</h4></div><div class='col-rght-6'>" + "<h4>Invoice Number : " + str(invoice_id) + " </h4>" +"<h4>Invoice Date : " + str(today.strftime('%d/%m/%y')) + "</h4>" +"<h4>Phone : " + str(inv.get("phone", 'No Phone Found')) + "</h4>" + "<h4>Fax : " + str(inv.get("fax", 'No Fax Found')) + "</h4></div></div></div>"

            html_4   = "<div class='container'><table cellpadding='0' cellspacing='0'><thead>" 
            html_5   = "<tr><th scope='col'>#</th><th>Username Name</th><th scope='col'>Date Ordered</th>" +"<th scope='col'>Reference</th><th scope='col'>Client Reference</th><th scope='col'>Disb.</th>" + "<th scope='col'>Charge</th><th scope='col'>Disb. & Charge</th><th scope='col'>GST Amount</th>" + "<th scope='col'>Disb. & Charge (GST Inc.)</th></tr><tbody>"


            inv = invs[len(invs) - 1]
            html_6         = "</tbody></table></div><div class='container'><div class='total-summary'><h4>" +"Disb. & Charge : <strong>" + str(disb_charge_total) + "</strong></h4>" +"<h4> Discount : " + str(inv.get("discount", 0)) + "</h4>" + f"<h4> Amount({str(disb_charge_total)}) - Discount {str(inv.get('discount', 0))}% : " + str(round(float(disb_charge_total) - float(disb_charge_total * inv["discount"]/100), 2)) + "</h4>" +"<h4> Taxes GST : " + str(round(inv["GST_total"],2)) + "</h4>" + "<h3> Total Invoice Amount : " + str(round(inv["GST_total"]+(float(disb_charge_total) - float(disb_charge_total * inv["discount"]/100)), 2)) + "</h3></div><hr>"
            
            html_7         = r'</div><div class="container"><div class="total-footer"><h4> <strong>Invoice Term : 7 Day Account</strong></h4><span><em>Please Note</em></h4></div> </div> <div class="container"><div class="abf-card"> <p> Payment can be made via credit card or cheque. Please ensure the "invoice Number" is quoted when frwarding or completing all payments via CC, EFT OR CHQ. ie: 71083 </p> <p> <strong>Banking Details</strong> </p> <p> Name : R. Hazlett & Co<br> Bank : COMMONWEALTH BANK<br> BSB : 062021<br> Account : 10244749 </p> <p> <strong>CARD NUMBER</strong>_ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _ _ _<br> <STRONG></STRONG> <strong>EXPIRY: _ _/_ _</strong> AMOUNT TO CHARGE : $__ __ </p> </div></div></div> <div class="container"><div class="invoice-footer"><span>Lvel4, 122 Castleregah Street Sydney 200-DX 1078 SYDNEY<span><br></br><STRONG>GPO BOX 96 SYDNEY</STRONG><br> <span>phone : 926515211 Fax : 02 92647752</pspan <br><span> R Hazlett & co ABN 20 104 470 340</span><br><span>www.hazlett.com.au</span><br> </p></div></div></div></body></html>'

            try:
                with open(file_name_1,"w") as html:
                    htm = html_head + html_1  + html_3 + html_4 +html_5 + html_2 + html_6 + html_7
                    html.write(htm)
                    html.close()
            except Exception as e:
                print(e)
            
            try:
                pdfkit.from_file(file_name_1, file_name_2)
            except Exception as e:
                print(e)
                
            shutil.copyfile(self.file_path_2 +'/'+ file_name_2, self.file_path_1 + "/files/" + file_name_2)
            invoice_paths.append(self.file_path_1 + "/files/" + file_name_2)
            new_folder      = random.randint(1,3910209312)
            final_folder    = '{path}/{folder}'.format(path=self.file_path, folder=new_folder)
            if not os.path.exists(final_folder):
                os.makedirs(final_folder)
            shutil.move(file_name_2, final_folder)

            f += 1

            table.pdf_link        = final_folder + '/' + file_name_2
            table.payment_status  = ""
            table.date_generated = timezone.now()
            table.save()

            new_items = ''
            for x in invoice_items:
                new_items = InvoiceItems.objects.create()
                for y in x.keys():
                    setattr(new_items,y,x[y])
                setattr(new_items, 'invoice', table)
                new_items.save()

            headers = {
                'Authorization': 'Bearer CIUi51PTEA4bPR9jksNecoG.6oJPNtkpKMyUf3CG4GTEtnYi',
                'FROM_ADMIN': 'Yes',
                'Content-type': 'application/json'
                }
                
            if inv["compemail1"] == None or inv["compemail1"] == '' or inv['compemail1'] == 'None':
                email = 'support.rubela.shome@gmail.com'
            else:
                email = inv.get("compemail1", "support.rubela.shome@gmail.com")
                
            data = {"id": table.id, "file_name": file_name_2, "comp_mail": email}

            response = requests.post(url=f"{settings.API_URL}/invoice/email",data=json.dumps(data), stream=True,headers=headers)

            
        return invoice_paths

    # Caller method to execute all other methods
    def generate_invoice(self, file_path):
        """
            Function to execute Invoice Gneerator methods
            paramter 1 : file path to create or store pdf
            returns invoice array
            
        """

        print("Generating invoice.........")
        self.setTransactionDate()
        invoice_array   = self.get_invoice_data()

        if len(invoice_array) > 0 :
            paths = self.invoice_generator(invoice_array, file_path)
        else :
            paths = ""

        # return invoice_array
        return paths




# @shared_task  (name="test")  
# @shared_task(name="sum_two_numbers")
# def add(x, y):
#     return x + y
# @shared_task  (name="invoice_generate") 
# def start():
    
#     rary = InvoiceGenerator(SwSearchMasterTbl, HazCustomerMasterTbl, Company, SwProductPricing, SwInvoice)
#     rary.generate_invoice(file_path, file_path_1)     