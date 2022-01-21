from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from typing import Optional

router=APIRouter(tags=["mylocal"])


#scehema
#1 subscribe
class subscribe(BaseModel):
   type:str
   email:Optional[str]=None
   mobile:Optional[str]=None
   notification:Optional[list]

#endpoint
#1 subscribe create


sql_data = [
   {'day':1,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(82).png'},
{'day':2,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(83).png'},
{'day':4,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(84).png'},
{'day':5,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(85).png'},
{'day':6,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(86).png'},
{'day':7,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(87).png'},
{'day':8,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(88).png'},
{'day':9,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(89).png'},
{'day':10,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(90).png'},
{'day':11,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(91).png'},
{'day':12,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(92).png'},
{'day':13,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(93).png'},
{'day':14,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(94).png'},
{'day':15,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(95).png'},
{'day':16,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(96).png'},
{'day':17,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(97).png'},
{'day':18,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(98).png'},
{'day':19,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(99).png'},
{'day':20,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(100).png'},
{'day':21,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(101).png'},
{'day':22,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(102).png'},
{'day':23,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(103).png'},
{'day':24,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(104).png'}
]
# @router.get("/mylocal")
# async def mylocal_create(request:Request):
   
#    for x in sql_data:
#       print(x['day'],x['link'])
#       #query set
#       query="""update blog set media_type='image',media_url=:media_url where type='hormonometer' and day=:day"""
#       values={"day":x['day'],"media_url":x['link']}
#       #query run
#       response=await database_execute(query,values)
#       print(response)
#       if response["status"]=="false":
#          raise HTTPException(status_code=400,detail=response)

#    return "rest"




@router.get("/mylocal")
async def mylocal_create(request:Request):
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
   msg['To'] = "manish@pingaweb.com"
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
   return "fdghjgfkjchgk"





# @router.get("/mylocal")
# async def mylocal_create(request:Request):
#    import boto3
#    from botocore.exceptions import ClientError

#    # Replace sender@example.com with your "From" address.
#    # This address must be verified with Amazon SES.
#    SENDER = "Sender Name <notify@pingaweb.com>"

#    # Replace recipient@example.com with a "To" address. If your account 
#    # is still in the sandbox, this address must be verified.
#    RECIPIENT = "manish@pingaweb.com"

#    # Specify a configuration set. If you do not want to use a configuration
#    # set, comment the following variable, and the 
#    # ConfigurationSetName=CONFIGURATION_SET argument below.

#    #CONFIGURATION_SET = "ConfigSet"

#    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
#    AWS_REGION = "us-west-2"

#    # The subject line for the email.
#    SUBJECT = "Amazon SES Test (SDK for Python)"

#    # The email body for recipients with non-HTML email clients.
#    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
#                "This email was sent with Amazon SES using the "
#                "AWS SDK for Python (Boto)."
#                )
               
#    # The HTML body of the email.
#    BODY_HTML = """<html>
#    <head></head>
#    <body>
#    <h1>Amazon SES Test (SDK for Python)</h1>
#    <p>This email was sent with
#       <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
#       <a href='https://aws.amazon.com/sdk-for-python/'>
#          AWS SDK for Python (Boto)</a>.</p>
#    </body>
#    </html>
#                """            

#    # The character encoding for the email.
#    CHARSET = "UTF-8"

#    # Create a new SES resource and specify a region.
#    client = boto3.client('ses',region_name=AWS_REGION)

#    # Try to send the email.
#    try:
#       #Provide the contents of the email.
#       response = client.send_email(
#          Destination={
#                'ToAddresses': [
#                   RECIPIENT,
#                ],
#          },
#          Message={
#                'Body': {
#                   'Html': {
#                      'Charset': CHARSET,
#                      'Data': BODY_HTML,
#                   },
#                   'Text': {
#                      'Charset': CHARSET,
#                      'Data': BODY_TEXT,
#                   },
#                },
#                'Subject': {
#                   'Charset': CHARSET,
#                   'Data': SUBJECT,
#                },
#          },
#          Source=SENDER,
#          # If you are not using a configuration set, comment or delete the
#          # following line

#          #ConfigurationSetName=CONFIGURATION_SET,
#       )
#    # Display an error if something goes wrong.	
#    except ClientError as e:
#       print(e.response['Error']['Message'])
#    else:
#       print("Email sent! Message ID:"),
#       print(response['MessageId'])
#    return "uyuytut"