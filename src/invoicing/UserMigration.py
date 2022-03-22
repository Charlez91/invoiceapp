from .models import AuthUser, UserEmail, Company
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.utils import timezone

def migrate(data):
    try:
        instance = AuthUser.objects.create(
            password = make_password(data["password"].upper()),
            username = data['username'].upper(),
            first_name = data['first_name'].upper(),
            last_name = data['last_name'].upper(),
            email= data['email'],
            is_staff=0,
            is_active=1,
            is_superuser=0,
            date_joined=timezone.now()
        )

        instance.save()

        message = {"status":True,"csv_id":data['id'], "message": f" Migrating Username with username {data['username']} and CSV ID {data['id']} Successs"}
        f = open("migration_logs.txt", "a")
        f.write(str(message))
        f.close()
        return message

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        html_error = f"""
            <tr>
            <td>Error</td>
            <td>{data['id']}</td>
            <td>{data['username']}</td>
            <td>{str(message)}
            </tr>
            """
        error = {"status":False,"csv_id":data['id'], "message": f"Error Migrating Username with username {data['username']} and CSV ID {data['id']}"
                ,"exception": message}
        f = open("migration_logs.txt", "a")
        f.write(str(error))
        f.close()

        error['html'] = html_error

        return error


def emailmigrate(data):
    try:

        user_instance = AuthUser.objects.get(username=data['username'].upper())
        email_instance = UserEmail.objects.create(user=user_instance.id, user_index=data['id'])
        email_instance.save()

        message = {"status":True,"csv_id":data['id'], "message": f" Migrating Email with username {data['username']} and CSV ID {data['id']} Successs"}
        return message


    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)

        html_error = f"""
            <tr>
            <td>Error</td>
            <td>{data['id']}</td>
            <td>{data['username']}</td>
            <td>{str(message)}
            </tr>
            """
        error = {"status":False,"csv_id":data['id'], "message": f"Error Migrating Email with username {data['username']} and CSV ID {data['id']}"
                ,"exception": message}

        f = open("migration_logs.txt", "a")
        f.write(str(error))
        f.close()

        error['html'] = html_error

        return error
        
def insertEmail(data):
    try:

        email_instance = UserEmail.objects.get(user_index=data['id'])
        email_instance.email = data['email']
        email_instance.first_name = data['fname']
        email_instance.last_name = data['lname']
        email_instance.title = data['title']

        email_instance.save()

        message = {"status":True, "csv_id":data['id'], "message": f"Success"}
        return message


    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)

        html_error = f"""
            <tr>
            <td>Error Inserting Details</td>
            <td>{data['id']}</td>
            <td>{data['email']}</td>
            <td>{str(message)}
            </tr>
            """
        error = {"status":False,"csv_id":data['id'], "message": f"Error Inserting Email with email {data['email']} and CSV ID {data['id']}"
                ,"exception": message}

        f = open("migration_logs.txt", "a")
        f.write(str(error))
        f.close()

        error['html'] = html_error

        return error

def updateCompany(data):
    try:

        company_instance = Company.objects.get(compcode=data['code'])
        company_instance.compemail1 = data['email']
        company_instance.companyindex = data['index']
        company_instance.save()

        message = {"status":True, "csv_id":data['index'], "message": f"Success"}
        return message


    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)

        html_error = f"""
            <tr>
            <td>Error Inserting Details</td>
            <td>{data['index']}</td>
            <td>{data['email']}</td>
            <td>{str(message)}
            </tr>
            """
        error = {"status":False,"csv_id":data['index'], "message": f"Error Inserting Email with email {data['email']} and CSV ID {data['index']}"
                ,"exception": message}

        f = open("migration_logs1.txt", "a")
        f.write(str(error))
        f.close()

        error['html'] = html_error

        return error