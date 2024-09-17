from imbox import Imbox
from datetime import datetime, timedelta
import pandas as pd
from barcode_reader import *
from openpyxl import Workbook
import os

username = 'seu_email'
password = open('password/token', 'r').read()
host = "imap.gmail.com"
download_folder = "boleto"

mail = Imbox(host, username= username,password= password, ssl=True)
messages = mail.messages(date__gt=datetime.today() - timedelta(days=20), raw='has:attachment')

for (uid, message) in messages:
    if len(message.attachments)>0:
        for attach in message.attachments:
            att_file = attach["filename"]

            if '.pdf' in att_file:
                download_path = f"{download_folder}/{att_file}"

                with open(download_path, 'wb') as fp:
                    fp.write(attach['content'].read())

                try:
                    barcode = BarcodeReader(download_path)
                    linha_dig = linha_digitavel(barcode)
                except:
                    barcode = False

            if not barcode:
                os.remove(download_path)
            else:
                print(message.subject, '-', linha_dig)
            
mail.logout()


