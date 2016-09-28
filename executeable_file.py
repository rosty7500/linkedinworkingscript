import csv
import main_file
import requests
import dns.resolver

with open('Import details for linkedin - Sheet1.csv') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        try:
            r = requests.get("http://www." +row[2])
            x = dns.resolver.query(row[2], 'MX')
            if len(x) == 5:
                value = main_file.generating_email(row)
                #print(value)
                print('Completed')
        except:
            print("Invalid domain")
            pass

