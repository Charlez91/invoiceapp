
import os, json
from invoicing.ingen import InvoiceGenerator
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .UserMigration import migrate as UserMigration
from .models import *
import csv
import io
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from invoicing.generator import Invoice as InGenerator
import requests
import base64
from django.http import FileResponse
def Welcome(request):
    return render(request, "welcome.html")

def Invoice(request):
    retrieveJSON = request.GET.get('json', False)
    data = {'sdate': request.GET['sdate'], 'edate': request.GET['edate']}
    file_path   = os.path.join(os.path.dirname(settings.BASE_DIR), "files")
    rary        = InvoiceGenerator(data, retrieveJSON)
    result      = rary.get_invoice_data()
    print(result)
    if result != "": 
        data["success"]    = "Invoice Generated"
        data["code"]    = "true"
        data["paths"]    = result
    else:
        data['code'] = "false"
        data["error"] = "No matching data on the database"

    return JsonResponse(data)

def migrate(request):
    with io.open('newCsv.csv','r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        error_count = 0
        success_count = 0
        html_errors = ''
        for row in csv_reader:
            instance = UserMigration(
                {
                    "username": f"{row[2]}+{row[1]}",
                    "password": row[3],
                    "email":"info@hazdev.com.au",
                    "first_name": row[1],
                    "last_name": row[2],
                    "id": row[0]
                }
            )
        
            print(f"Processed Lines {line_count}")
            line_count += 1

            if instance['status'] == False:
                print(f"Error Count {error_count}")
                error_count += 1
                html_errors += mark_safe(instance['html'])

            else:
                print(f"Success Count {success_count}")
                success_count += 1

        csv_file.__exit__()
        f = open(os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates") + '/base_logs_1.html', "w")
        html = render_to_string('base_logs.html', {'table_data': mark_safe(html_errors)})
        f.write(html)
        f.close()
        return render(request,'base_logs_1.html')

def view_latest_log(request):
    return render(request,'real_logs.html')

def view_latest_log_company(request):
    return render(request,'real_logs_new.html')

@csrf_exempt
def check_password(request):
    try:
        html = render_to_string('base_logs_1.html', {'table_data': "none"})
        return JsonResponse({"status": request.POST['password'] == "thisisthepassword", "body": html})
    except Exception:
        return JsonResponse({"status": False})

@csrf_exempt
def check_password_next(request):
    try:
        html = render_to_string('base_logs_2.html', {'table_data': "none"})
        return JsonResponse({"status": request.POST['password'] == "thisisthepassword", "body": html})
    except Exception:
        return JsonResponse({"status": False})

def getInvoiceFile(request):
    invoice_id = request.GET.get("id",None)
    if invoice_id == None:
        return JsonResponse({"message": "File not Found"})
    
    file = SwInvoice.objects.get(id=invoice_id)
    return FileResponse(open(file.pdf_link.path, 'rb'), content_type='application/pdf')


def viewInvoiceFile(request):
    invoice_id = request.GET.get("id",None)
    if invoice_id == None:
        return JsonResponse({"message": "File not Found"})
    
    file = SwInvoice.objects.get(id=invoice_id)
    datapdf = ''

    with open(file.pdf_link.path, 'rb') as pdf:
        datapdf = base64.b64encode(pdf.read()).decode('ascii')
    return render(request, "pdf.html", {"data": datapdf})

def invoiceGenerate(request):
    invoice_id = request.GET.get('id', None)

    if invoice_id == None or invoice_id == '':
        return JsonResponse({"message": "Invalid Invoice ID Passed"})

    generator = InGenerator()
    res = generator.update(id=invoice_id)
    
    headers = {
			'Authorization': 'Bearer CIUi51PTEA4bPR9jksNecoG.6oJPNtkpKMyUf3CG4GTEtnYi',
			'FROM_ADMIN': 'Yes',
            'Content-type': 'application/json'
		}
    
    company_instance = Company.objects.get(compcode=res.cmpany_code)
    email = ''
    if company_instance.compemail1 == None or company_instance.compemail1 == '' or company_instance.compemail1 == 'None':
        email = 'support.rubela.shome@gmail.com'
    else:
        email = company_instance.compemail1
    data = {}
    if int(settings.REAL_EMAIL) == 1:
        data = {"id": res.id, "file_name": "invoice.pdf", "comp_mail": email}
    else:
        data = {"id": res.id, "file_name": "invoice.pdf", "comp_mail": settings.DEMO_EMAIL}

    if str(settings.DEV).lower() == 'no':
        response = requests.post(url=f"{settings.API_URL}/invoice/email",data=json.dumps(data), stream=True,headers=headers)

    return JsonResponse({"data": "Invoice reissued successfully"})


def getInvoiceRawFile(request):
    invoice_id = request.GET.get("id",None)
    if invoice_id == None:
        return JsonResponse({"message": "File not Found", "status": True})
    
    file = SwInvoice.objects.get(id=invoice_id)
    response = HttpResponse(file.pdf_link, content_type='application/pdf')
    response['Content-Disposition'] = "inline"
    return response