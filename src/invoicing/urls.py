"""invoicing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Invoice, Welcome, migrate, view_latest_log,view_latest_log_company, check_password, getInvoiceFile,check_password_next, invoiceGenerate, getInvoiceRawFile, viewInvoiceFile
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Welcome, name="Welcome"),
    path('welcome/', Welcome, name="Welcome"),
    path('invoice/', Invoice, name='Invoice'),
    path('migrate/user', migrate, name='migrate'),
    path('migrate/user/logs', view_latest_log, name='view_migration_logs'),
    path('migrate/company/logs', view_latest_log_company, name='view_latest_log_company'),
    path('password/logs/check', check_password),
     path('password/logs/check/company', check_password_next),
    path('file_download/', getInvoiceFile),
    path('file_view/', viewInvoiceFile),
    path('invoice/update', invoiceGenerate),
    path('invoice/download', getInvoiceRawFile),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
