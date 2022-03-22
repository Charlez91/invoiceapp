# from __future__ import absolute_import, unicode_literals  
  
# import os  
# from celery import Celery  
# from celery.schedules import crontab  
  
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_project.settings')  


  
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SydWater.settings') 
# # file_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src")

# # celery settings for the demo_project  
# app = Celery('sydWater')  
# app.config_from_object('django.conf:settings', namespace='CELERY')  
# # here is the beat schedule dictionary defined  
# app.conf.beat_schedule = {  
#     'print-every-friday': {  
#         'task': 'product.task.start',  
#         'schedule': crontab(hour=14, minute=28, day_of_week=2), 
#         'args'      : ("working") 
#         # 'args': (SwSearchMasterTbl, HazCustomerMasterTbl, Company, SwProductPricing, SwInvoice, file_path)  
# },  
# }  
  
# app.autodiscover_tasks()  

from __future__ import absolute_import, unicode_literals # for python2

import os
from celery import Celery
from celery.schedules import crontab 
from django.conf import settings 

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoicing.settings') 


## Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6380')
file_path   = os.path.join(os.path.dirname(settings.BASE_DIR), "src")

app = Celery('invoicing')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY') 

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
app.conf.timezone = 'UTC'
app.conf.beat_schedule = {  
    'add-every-minute-contrab': {
        'task': 'invoice_generate',
        'schedule': crontab(hour=18, minute=30, day_of_week=0),
        'args': (file_path),
    },
} 