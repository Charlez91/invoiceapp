#Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import random
import os
from django.utils import timezone

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserTemp(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user_temp'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Company(models.Model):
    companyindex = models.IntegerField(db_column='companyIndex', primary_key=True)  # Field name made lowercase.
    companyid = models.IntegerField(db_column='companyId')  # Field name made lowercase.
    compname = models.CharField(db_column='compName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compcode = models.CharField(db_column='compCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    compstreet = models.CharField(db_column='compStreet', max_length=255, blank=True, null=True)  # Field name made lowercase.
    compsuburb = models.CharField(db_column='compSuburb', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compstate = models.CharField(db_column='compState', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comppostcode = models.CharField(db_column='compPostcode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    compphone1 = models.CharField(db_column='compPhone1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailstreet = models.CharField(db_column='mailStreet', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mailsuburb = models.CharField(db_column='mailSuburb', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailstate = models.CharField(db_column='mailState', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mailpostcode = models.CharField(db_column='mailPostcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    directcontact = models.CharField(db_column='directContact', max_length=100, blank=True, null=True)  # Field name made lowercase.
    directcontactnumber = models.CharField(db_column='directContactNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    directcontactmobile = models.CharField(db_column='directContactMobile', max_length=30, blank=True, null=True)  # Field name made lowercase.
    directfaxnumber = models.CharField(db_column='directFaxNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupId', blank=True, null=True)  # Field name made lowercase.
    faxnumberareacode = models.CharField(db_column='faxNumberAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    compfax1 = models.CharField(db_column='compFax1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    compemail1 = models.CharField(db_column='compEmail1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    compdirectphonenumberareacode = models.CharField(db_column='compDirectPhoneNumberAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    comphomephonenumberareacode = models.CharField(db_column='compHomePhoneNumberAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    clientonline = models.IntegerField(blank=True, null=True)
    groupidmanual = models.IntegerField(db_column='groupIdManual', blank=True, null=True)  # Field name made lowercase.
    companyacn = models.CharField(db_column='CompanyACN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    companyabn = models.CharField(db_column='CompanyABN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    msrepl_tran_version = models.CharField(max_length=10, blank=True, null=True)
    markfordeletion = models.IntegerField(db_column='MarkForDeletion', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    directcontactareacode = models.CharField(db_column='directContactAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    settlementclient = models.IntegerField(db_column='SettlementClient', blank=True, null=True)  # Field name made lowercase.
    # iquoteenabled = models.TextField(db_column='iQuoteEnabled', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    dxnumber = models.CharField(db_column='DXNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dxexchange = models.CharField(db_column='DXExchange', max_length=20, blank=True, null=True)  # Field name made lowercase.
    billingmethod = models.IntegerField(db_column='BillingMethod', blank=True, null=True)  # Field name made lowercase.
    column1 = models.CharField(db_column='COLUMN1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column2 = models.CharField(db_column='COLUMN2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column3 = models.CharField(db_column='COLUMN3', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column4 = models.CharField(db_column='COLUMN4', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column5 = models.CharField(db_column='COLUMN5', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column6 = models.CharField(db_column='COLUMN6', max_length=100, blank=True, null=True)  # Field name made lowercase.
    discount = models.ForeignKey('DiscountTbl', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class DiscountTbl(models.Model):
    discount = models.FloatField()
    companies_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount_tbl'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.PositiveIntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.IntegerField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoCeleryResultsChordcounter(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    sub_tasks = models.TextField()
    count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_chordcounter'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HazCustomerMasterTbl(models.Model):
    customer_code = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'haz_customer_master_tbl'


class HazUserSessions(models.Model):
    login_id = models.AutoField(primary_key=True)
    jwt_token = models.CharField(max_length=416, blank=True, null=True)
    customerid = models.ForeignKey(HazCustomerMasterTbl, models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    blacklisted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'haz_user_sessions'


class Oauth2Client(models.Model):
    client_secret = models.CharField(max_length=120, blank=True, null=True)
    client_id_issued_at = models.IntegerField()
    client_secret_expires_at = models.IntegerField()
    client_metadata = models.TextField(blank=True, null=True)
    user = models.ForeignKey(HazCustomerMasterTbl, models.DO_NOTHING, blank=True, null=True)
    client_id = models.CharField(max_length=48, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_client'


class Oauth2Code(models.Model):
    code = models.CharField(unique=True, max_length=120)
    client_id = models.CharField(max_length=48, blank=True, null=True)
    redirect_uri = models.TextField(blank=True, null=True)
    response_type = models.TextField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    nonce = models.TextField(blank=True, null=True)
    auth_time = models.IntegerField()
    code_challenge = models.TextField(blank=True, null=True)
    code_challenge_method = models.CharField(max_length=48, blank=True, null=True)
    user = models.ForeignKey(HazCustomerMasterTbl, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_code'


class Oauth2Token(models.Model):
    client_id = models.CharField(max_length=48, blank=True, null=True)
    token_type = models.CharField(max_length=40, blank=True, null=True)
    access_token = models.CharField(unique=True, max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    revoked = models.IntegerField(blank=True, null=True)
    issued_at = models.IntegerField()
    expires_in = models.IntegerField()
    user = models.ForeignKey(HazCustomerMasterTbl, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_token'


class SwCustomerPayloadTbl(models.Model):
    customerid = models.CharField(db_column='customerId', primary_key=True, max_length=30)  # Field name made lowercase.
    orderid = models.CharField(db_column='orderId', max_length=40)  # Field name made lowercase.
    currentownername = models.CharField(db_column='currentOwnerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    applicantreferencenumber = models.CharField(db_column='applicantReferenceNumber', max_length=12, blank=True, null=True)  # Field name made lowercase.
    section66 = models.IntegerField()
    sewerservicediagram = models.IntegerField(db_column='sewerServiceDiagram')  # Field name made lowercase.
    servicelocationprint = models.IntegerField(db_column='serviceLocationPrint')  # Field name made lowercase.
    buildingoveroradjacenttosewer = models.IntegerField(db_column='buildingOverOrAdjacentToSewer')  # Field name made lowercase.
    specialmeterreading = models.IntegerField(db_column='specialMeterReading')  # Field name made lowercase.
    section88g = models.IntegerField(db_column='section88G')  # Field name made lowercase.
    lotnumber = models.CharField(db_column='lotNumber', max_length=9, blank=True, null=True)  # Field name made lowercase.
    plantype = models.CharField(db_column='planType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    plannumber = models.CharField(db_column='planNumber', max_length=9, blank=True, null=True)  # Field name made lowercase.
    sectionnumber = models.CharField(db_column='sectionNumber', max_length=4, blank=True, null=True)  # Field name made lowercase.
    propertyunitnumber = models.CharField(db_column='propertyUnitNumber', max_length=4, blank=True, null=True)  # Field name made lowercase.
    propertyaddressstreetnumber = models.CharField(db_column='propertyAddressStreetNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    propertyaddressstreetname = models.CharField(db_column='propertyAddressStreetName', max_length=24, blank=True, null=True)  # Field name made lowercase.
    propertyaddresssuburb = models.CharField(db_column='propertyAddressSuburb', max_length=31, blank=True, null=True)  # Field name made lowercase.
    propertyaddresspostcode = models.CharField(db_column='propertyAddressPostcode', max_length=4, blank=True, null=True)  # Field name made lowercase.
    municipality = models.CharField(max_length=30, blank=True, null=True)
    propertytype = models.CharField(db_column='propertyType', max_length=3, blank=True, null=True)  # Field name made lowercase.
    overridedatavalidation = models.IntegerField(db_column='overrideDataValidation', blank=True, null=True)  # Field name made lowercase.
    referencenumber = models.CharField(db_column='referenceNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    otherreferences = models.CharField(db_column='otherReferences', max_length=100, blank=True, null=True)  # Field name made lowercase.
    internal_username = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_customer_payload_tbl'
        unique_together = (('customerid', 'orderid'),)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_pdf_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Invoices/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class SwInvoice(models.Model):
    invoice_id = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    cmpany_code = models.CharField(max_length=100)
    searches_from = models.DateField(db_column='Searches_From', blank=True, null=True)  # Field name made lowercase.
    searches_to = models.DateField(db_column='Searches_To', blank=True, null=True)  # Field name made lowercase.
    searches_no = models.CharField(db_column='Searches_No', blank=True, null=True, max_length=100)  # Field name made lowercase.
    search_charge = models.FloatField(db_column='Search_Charge', blank=True, null=True)  # Field name made lowercase.
    service_charge = models.FloatField(db_column='Service_Charge', blank=True, null=True)  # Field name made lowercase.
    gst_charge = models.FloatField(db_column='GST_charge')  # Field name made lowercase.
    total_price = models.FloatField()
    pdf_link = models.FileField(upload_to=upload_pdf_path, null=True, blank=True)  # Field name made lowercase.
    payment_status = models.CharField(max_length=100)
    date_generated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'sw_invoice'


class SwProductPricing(models.Model):
    product_code = models.CharField(primary_key=True, max_length=8)
    product_description = models.CharField(max_length=100)
    product_price = models.FloatField(blank=True, null=True)
    product_gst_fees = models.CharField(max_length=10)
    sw_product_fees = models.FloatField(blank=True, null=True)
    sw_product_gst_fees = models.CharField(max_length=10)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_product_pricing'


class SwProductsTbl(models.Model):
    product_code = models.CharField(primary_key=True, max_length=8)
    product_description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'sw_products_tbl'


class SwPropertyTypesTbl(models.Model):
    propertytype_code = models.IntegerField(blank=True, null=True)
    propertytype_description = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'sw_property_types_tbl'


class SwSearchArtefactsTbl(models.Model):
    haz_order_id = models.CharField(max_length=40)
    n_appn = models.CharField(db_column='N_APPN', max_length=12, blank=True, null=True)  # Field name made lowercase.
    processing_status = models.CharField(max_length=12, blank=True, null=True)
    directory_unprocessed = models.CharField(max_length=200, blank=True, null=True)
    filename_unprocessed = models.CharField(max_length=100, blank=True, null=True)
    directory_processed = models.CharField(max_length=200, blank=True, null=True)
    filename_processed = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_search_artefacts_tbl'


class SwSearchMasterTbl(models.Model):
    id = models.IntegerField(unique=True)
    haz_order_id = models.CharField(primary_key=True, max_length=50)
    customer_code = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=45)
    order_datetime = models.DateTimeField(blank=True, null=True)
    currentownername = models.CharField(db_column='currentOwnerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    applicantreferencenumber = models.CharField(db_column='applicantReferenceNumber', max_length=12, blank=True, null=True)  # Field name made lowercase.
    otherreferences = models.CharField(db_column='otherReferences', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lotnumber = models.CharField(db_column='lotNumber', max_length=9, blank=True, null=True)  # Field name made lowercase.
    depositedplannumber = models.CharField(db_column='depositedPlanNumber', max_length=9, blank=True, null=True)  # Field name made lowercase.
    strataplannumber = models.CharField(db_column='strataPlanNumber', max_length=7, blank=True, null=True)  # Field name made lowercase.
    sectionnumber = models.CharField(db_column='sectionNumber', max_length=4, blank=True, null=True)  # Field name made lowercase.
    unitnumber = models.CharField(db_column='unitNumber', max_length=4, blank=True, null=True)  # Field name made lowercase.
    streetnumber = models.CharField(db_column='streetNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    streetname = models.CharField(db_column='streetName', max_length=24, blank=True, null=True)  # Field name made lowercase.
    suburb = models.CharField(max_length=31, blank=True, null=True)
    postcode = models.CharField(db_column='postCode', max_length=4, blank=True, null=True)  # Field name made lowercase.
    municipality = models.CharField(max_length=30, blank=True, null=True)
    propertytype = models.CharField(db_column='propertyType', max_length=3, blank=True, null=True)  # Field name made lowercase.
    propertynumber = models.CharField(db_column='propertyNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    applicationid = models.CharField(db_column='applicationId', max_length=14, blank=True, null=True)  # Field name made lowercase.
    application_status = models.CharField(max_length=20, blank=True, null=True)
    productid = models.CharField(db_column='productId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    product_status = models.CharField(max_length=30, blank=True, null=True)
    document_retrieval_tries = models.IntegerField(blank=True, null=True)
    application_submission_tries = models.IntegerField(blank=True, null=True)
    order_details = models.CharField(max_length=300, blank=True, null=True)
    document_url = models.CharField(max_length=2083, blank=True, null=True)
    staff_comments = models.CharField(max_length=200, blank=True, null=True)
    internal_username = models.CharField(max_length=60, blank=True, null=True)
    date_closed = models.DateTimeField(null=True)
    class Meta:
        managed = False
        db_table = 'sw_search_master_tbl'
        unique_together = (('haz_order_id', 'product_name'),)


class SwSearchTransactionHistoryTbl(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    job_id = models.IntegerField()
    haz_order_id = models.CharField(max_length=40)
    product_code = models.CharField(max_length=8)
    n_appn = models.CharField(db_column='N_APPN', max_length=12, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=30, blank=True, null=True)
    validation_error = models.CharField(max_length=200, blank=True, null=True)
    fatal_error = models.CharField(max_length=200, blank=True, null=True)
    unprocessedrsp_location = models.CharField(max_length=200, blank=True, null=True)
    document_location = models.CharField(max_length=200, blank=True, null=True)
    notification_message = models.CharField(max_length=200, blank=True, null=True)
    resolution_time = models.CharField(max_length=5, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    requestor_notified = models.IntegerField(blank=True, null=True)
    data_processed = models.IntegerField(blank=True, null=True)
    document_delivered = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_search_transaction_history_tbl'


class SwSearchTransactionTbl(models.Model):
    job_id = models.AutoField(primary_key=True)
    haz_order_id = models.CharField(max_length=40)
    product_code = models.CharField(max_length=8)
    n_appn = models.CharField(db_column='N_APPN', max_length=12, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=30, blank=True, null=True)
    validation_error = models.CharField(max_length=200, blank=True, null=True)
    fatal_error = models.CharField(max_length=200, blank=True, null=True)
    unprocessedrsp_location = models.CharField(max_length=200, blank=True, null=True)
    document_location = models.CharField(max_length=200, blank=True, null=True)
    notification_message = models.CharField(max_length=200, blank=True, null=True)
    resolution_time = models.CharField(max_length=5, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    requestor_notified = models.IntegerField(blank=True, null=True)
    data_processed = models.IntegerField(blank=True, null=True)
    document_delivered = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_search_transaction_tbl'


class UserCustomer(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    order_status = models.CharField(max_length=30)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user')
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company')

    class Meta:
        managed = False
        db_table = 'user_customer'


class InvoiceItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField(null=True)
    username = models.CharField(max_length=100, null=True)
    date_ordered = models.DateField(null=True)
    reference = models.CharField(max_length=100, null=True)
    client_reference = models.CharField(max_length=100, null=True)
    disb = models.FloatField(null=True)
    charge = models.FloatField(null=True)
    disb_charge = models.FloatField(null=True)
    gst_amount = models.FloatField(null=True)
    gst_inc = models.FloatField(null=True)
    include = models.BooleanField(default=True)
    transaction= models.IntegerField(null=True)
    invoice = models.ForeignKey(SwInvoice, on_delete=models.CASCADE, null=True)
    date_closed = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'invoice_items'

class UserEmail(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.IntegerField(null=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    user_index = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)

    class Meta:
        managed = False
        db_table = 'user_email'