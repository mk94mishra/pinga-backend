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


# for production ---

# sql_data = [
#    {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/lovely-couple-have-warm-cuddle.jpg','id':114},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/couple-talking-about-something-last-night-morning_1150-4965.jpg','id':115},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/he-loves-waking-up-his-love_329181-13854.jpg','id':116},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/portrait-expressive-young-woman.jpg','id':112},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/my-bed-is-my-best-friend.jpg','id':123},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/smiling-lovely-woman-holding-present-box-looking-away_171337-12660.jpg','id':124},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/overweight-squeeze-belly-fat-with-measure-tape-her-neck_1150-34777.jpg','id':125},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/beautiful-young-woman-eating-salad-black-background_1301-7563.jpg','id':126},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/weight-loss-scale-with-centimeter-top-view_1150-42311.jpg','id':128},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/shallow-focus-shot-sporty-female-doing-workout-park_181624-53286.jpg','id':129},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/sporty-woman-eats-red-apple-orange-wall_197531-13152.jpg','id':130},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/sick-woman-with-hands-stomach-suffering-from-intense-pain_1262-18659.jpg','id':131},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/pleased-satisfied-young-female-model-makes-zero-gesture-wears-transparent-glasses-has-long-dark-hair_273609-17999.jpg','id':132},	
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-asian-woman-practicing-yoga-living-room_7861-1619.jpg','id':136},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/medium-shot-woman-drinking-water_23-2149235399.jpg','id':137},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-woman-doing-her-workout-home-fitness-mat_23-2148995636.jpg','id':139},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/i-always-have-bottle-water-after-workout_329181-3555.jpg','id':140},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/portrait-happy-healthy-fitness-woman-holding-green-apple_171337-10200.jpg','id':141},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/funny-curly-haired-european-woman-blows-cheeks-has-fun-never-looses-sense-humor-holds-breath-makes-grimace-dressed-basic-t-shirt-isolated-white-wall-people-emotions-concept_273609-49632+(1).jpg','id':142},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/hopeful-cheerful-woman-crosses-fingers-good-luck-keeps-eyes-closed-smiles-pleasantly-applies-green-spa-facial-mask-reducing-fine-lines-wears-headband-stands-bare-shoulders-isolated-beige_273609-56958.jpg','id':144},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/healthy-lifestyle-medicine-nutritional-supplements-people-concept-close-up-male-hands-holding-pills-with-cod-liver-oil-capsules-water-glass_1088-1053.jpg','id':145},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/smiling-green-eyed-girl-puts-cream-clean-face-brunette-white-top-posing-isolated-wall_197531-13902.jpg','id':146},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/make-up-spa-treatment-concept_23-2148645530.jpg','id':150},
				
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-woman-hand-holding-pregnancy-test_1150-5119.jpg','id':152},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/dissatisfied-girl-keeps-hands-crotch-presses-lower-abdomen-needs-toilet-badly-has-syndrome-cystitis_273609-25635.jpg','id':153},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-woman-being-confident-with-her-acne_23-2148982594.jpg','id':154},
				
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/romantic-happy-couple-bed-enjoying-sensual-foreplay_1150-4957.jpg','id':158},
				
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/woman-having-stomach-ache-bending-with-hands-belly-discomfort-from-menstrual-cramps_1258-19063.jpg','id':160},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-woman-haviing-abdominal-pain-because-menstruation-lying-couch-holding-her-stomach_231208-689.jpg','id':161},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/woman-standing-with-stomach-ache-presses-her-hand-her-stomach_1150-25976.jpg','id':162},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/marijuana-buds-with-marijuana-joints-cannabis-oil_1150-20687.jpg','id':127},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-african-american-woman-dressed-sport-bra-eating-chocolate-after-workout-isolated-yellow-background_574295-1972.jpg','id':147},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/doctor-with-measure-tape-measuring-size-patient-s-breast_1301-7531.jpg','id':148},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/hand-holding-blood-glucose-meter-measuring-blood-sugar-background-is-stethoscope-chart-file_1387-942.jpg','id':155},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/puzzled-guilty-woman-white-dress-clinging-head-looking-female-periods-calendar-checking-menstruation-days_365776-3419.jpg','id':163},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/girl-feeling-sick-touching-stomach-complaining-cramps-pain_176420-30929.jpg','id':164},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/young-woman-holding-condom-contraceptive-pills-prevent-pregnancy_1150-14218.jpg','id':165},
# {'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blogs/smiling-beautiful-woman-approves-using-menstrual-cup-makes-okay-gesture-holds-silicone-product-insert-into-vagina-hand-gives-recommendations-women-begginer-cup-users-isolated-yellow_273609-39665.jpg','id':171}
# ]



import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

@router.get("/mylocal")
async def mylocal_create(request:Request):
   try:
      mailchimp = MailchimpTransactional.Client('877cb4df376f85992cb453bfe707bcb1-us20')
      response = mailchimp.users.ping()
      print('API called successfully: {}'.format(response))
      return 'API called successfully'
   except ApiClientError as error:
      print('An exception occurred: {}'.format(error.text))
      return 'An exception occurred:'

   
#    for x in sql_data:
#       print(x['id'],x['link'])
#       #query set
#       query="""update blog set media_type='image',media_url=:media_url where type='collection' and id=:id"""
#       values={"id":x['id'],"media_url":x['link']}
#       #query run
#       response=await database_execute(query,values)
#       print(response)
#       if response["status"]=="false":
#          raise HTTPException(status_code=400,detail=response)

#    return "rest"




# @router.get("/mylocal")
# async def mylocal_create(request:Request):
#    # import necessary packages

#    from email.mime.multipart import MIMEMultipart
#    from email.mime.text import MIMEText
#    import smtplib
#    from smtplib import SMTPException

#    # create message object instance
#    msg = MIMEMultipart()


#    message = "Thank you"

#    # setup the parameters of the message
#    password = "BLWYNd5wGkFn9db7B5BI4wkXZ64747MiVRzpxgP4FdN4"
#    msg['From'] = "notify@pingaweb.com"
#    msg['To'] = "manish@pingaweb.com"
#    msg['Subject'] = "My Account Setup PingaWeb"

#    # add in the message body
#    msg.attach(MIMEText(message, 'plain'))

#    #create server
#    server = smtplib.SMTP('email-smtp.ap-south-1.amazonaws.com: 587')

#    server.starttls()

#    # Login Credentials for sending the mail
#    server.login('AKIA22OPN45J7UZ6INNP', password)


#    # send the message via the server.
#    # print(server.sendmail(msg['From'], msg['To'], msg.as_string()))
#    try:
#       server.sendmail(msg['From'], msg['To'], msg.as_string())         
#       print("Successfully sent email")
#    except SMTPException:
#       print(SMTPException)
#    server.quit()
#    return "fdghjgfkjchgk"





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