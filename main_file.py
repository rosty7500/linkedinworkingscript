import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from validate_email import validate_email
import socket
import smtplib
import dns.resolver
import time

def generating_email(fetched_data):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('linkedin-5252e8f990b3.json', scope)
        gc = gspread.authorize(credentials)
        print("Connection successful to the Spreadsheet")
        worksheet = gc.open('Email Permutator1')
        ws = worksheet.worksheet('Sheet1')
        ws.update_acell('B1',fetched_data[0])
        ws.update_acell('B3',fetched_data[1])
        ws.update_acell('B4',fetched_data[2])
        generated_emails = ws.col_values(7)
        print (generated_emails)
        i = 0
        valid_email = 0
        num=len(generated_emails)
        while i < num and valid_email == 0:
            #for records in generated_emails:
            code = verifying_emails(generated_emails[i],fetched_data)
            if code == 250:
                valid_email = 1
            i=1+i
            #print(i)
            #print ("There is sleep here")
            time.sleep(1)
        return valid_email


def verifying_emails(records,fetched_data):
        email_details={}
        domain=fetched_data[2]
        record = dns.resolver.query(domain, 'MX')
        mxRecord = record[0].exchange
        mxRecord = str(mxRecord)

        # Get local server hostname
        host = socket.gethostname()

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(str(records))
        server.quit()
        print(code , records)
        email_details['Email']= records
        email_details['Status']= code


        with open('names.csv', 'a', newline='') as csvfile:
            fieldnames = ['Email', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(email_details)

        return code









