import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content('All is Good, Everything is working fine')

msg['Subject'] = 'This is test message'
msg['From'] = "nakulsharma8698@gmail.com"
msg['To'] = "shiv.ahuja1494@gmail.com"

# Send the message via our own SMTP server.
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("nakulsharma8698@gmail.com", "dscpbwposkgdqgbv")
server.send_message(msg)
server.quit()