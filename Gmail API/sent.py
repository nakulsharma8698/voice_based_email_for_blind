import smtplib
import time
import imaplib
import email
import os
import traceback 
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "nakulsharma8698" + ORG_EMAIL 
FROM_PWD = "dscpbwposkgdqgbv" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('"[Gmail]/Sent Mail"') #''

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1)[:5]:
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_to = msg['to']
                    auth_results = msg.get("Authentication-Results", None)
                    
                    content_type = msg.get_content_type()

                    body = msg.get_payload()
                    print(body)

                    if msg.is_multipart():
                # iterate over email parts
                        for part in msg.walk():
                    # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                        # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                               
                                #print(content_type)
                                print(body)
                               
                            """elif "attachment" in content_disposition:
                        # download attachment
                                filename = part.get_filename()
                                if filename:
                                    folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                    filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                                    open(filepath, "wb").write(part.get_payload(decode=True))"""
                    #body = mail[0].as_string()
                    #parts=payload.parts
                    """parts = payload.get('parts')[0]
                    data = parts['body']['data']
                    data = data.replace("-","+").replace("_","/")
                    decoded_data = base64.b64decode(data)"""
                    print('From : ' + email_from + '\n')
                    if(email_to):
                        print('To : ' + email_to + '\n')
                    if(email_subject):
                        print('Subject : ' + email_subject + '\n')
                    print(content_type+ '\n')
                    print('#############')
                    
                    #if(content_type == "text/plain"):
                    #   print(body)

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

read_email_from_gmail()