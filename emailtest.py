# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPException

# create message object instance
msg = MIMEMultipart()


message = "Thank you"

# setup the parameters of the message
password = "BLWYNd5wGkFn9db7B5BI4wkXZ64747MiVRzpxgP4FdN4"
msg['From'] = "notify@pingaweb.com"
msg['To'] = "mk94mishra@gmail.com"
msg['Subject'] = "My Account Setup PingaWeb"

# add in the message body
msg.attach(MIMEText(message, 'plain'))

#create server
server = smtplib.SMTP('email-smtp.ap-south-1.amazonaws.com: 587')

server.starttls()

# Login Credentials for sending the mail
server.login('AKIA22OPN45J7UZ6INNP', password)


# send the message via the server.
# print(server.sendmail(msg['From'], msg['To'], msg.as_string()))
try:
    server.sendmail(msg['From'], msg['To'], msg.as_string())         
    print("Successfully sent email")
except SMTPException:
    print(SMTPException)
server.quit()
   