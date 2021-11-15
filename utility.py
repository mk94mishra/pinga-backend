from setting import *
import json
import uuid
import boto3

#1 public endpoint check
async def is_public_endpoint(request):
   response={"status":"false"}
   request_url_resource="/".join(str(request.url).split("/")[3:])
   if (request.method,request_url_resource) in endpoint_public:
      response={"status":"true"}
   return response

#2 has valid token
import time,jwt
async def has_valid_token(request):
   #prework
   response={"status":"false"}
   authorization=request.headers.get("Authorization")
   #no auth
   if authorization==None:
      response={"status":"false","message":"no token found"}
      return response
   # no proper auth format
   authorization_split=authorization.split(" ")
   if len(authorization_split)!=2:
      response={"status":"false","message":"pls send <Bearer> <token>"}
      return response
   # no proper auth format
   if authorization_split[0]!="Bearer":
      response={"status":"false","message":"pls send <Bearer> <token>"}
      return response
   #token decode
   token=authorization_split[1]
   try:
      claims=jwt.decode(token,config['token_secret_key'], algorithms=["HS256"])
   except Exception as e:
      response={"status":"false","message":e.args}
      return response
   #finally
   response={"status":"true","message":claims}
   return response

#3 token create
from datetime import datetime, timedelta
def token_create(user_id):
   exp=datetime.now() + timedelta(days=2)           
   payload={'user_id':user_id,'exp':exp}
   key=config['token_secret_key']
   token=jwt.encode(payload,key)
   return token

#4 password hash create
import hashlib
def password_hash_create(password):
   password_hash = hashlib.md5(password.encode()).hexdigest()
   return password_hash

#5 database objects into list of dict
def database_object_converter(database_object):
   row_list=list(map(lambda x:dict(x),database_object))
   response=list()
   for row_single in row_list:
      if 'data' in row_single.keys() and row_single['data']!=None:
         row_single ['data']=json.loads(row_single ['data'])
      response.append(row_single )
   return response

#6 database:fetch all
async def database_fetch_all(query,values):
   response={"status":"false"}
   try:
      database_object=await database.fetch_all(query=query,values=values)
      #await database.disconnect()
   except Exception as e:
      response={"status":"false","message":e.args}
      return response
   row=database_object_converter(database_object)
   response={"status":"true","message":row}
   return response

#7 database:execute
async def database_execute(query,values):
   response={"status":"false"}
   try:
      await database.execute(query=query,values=values)
      #await database.disconnect()
   except Exception as e:
      response={"status":"false","message":e.args}
      return response
   response={"status":"true","message":"database operation successfull"}
   return response


#8 database:execute many
async def database_execute_many(query,values):
   response={"status":"false"}
   try:
      await database.execute_many(query=query,values=values)
      #await database.disconnect()
   except Exception as e:
      response={"status":"false","message":e.args}
      return response
   response={"status":"true","message":"database operation successfull"}
   return response

   

#9  admin user check
from setting import database
async def is_admin(user_id):
   #prework
   response={"status":"false"}
   #query set
   query="""select type from "user" where id=:id"""
   values={"id":user_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      return response
   user=response["message"][0]
   if user['type']!='admin':
      response={"status":"false","message":"you are not an admin"}
      return response
   response={"status":"true","message":"you are an admin"}
   return response



# s3 upload
async def get_presigned_url(filename_with_extension,user_id):
    #unique s3 key
    key=str(uuid.uuid4())+"_"+str(user_id)+"_"+filename_with_extension
    #s3 client
    s3_client=boto3.client(config["aws_service"],region_name=config["region_name"],aws_access_key_id=config["aws_access_key_id"],aws_secret_access_key=config["aws_secret_access_key"])
    #generate presigned post url
    response=s3_client.generate_presigned_post(Bucket=config["s3_bucket_name"],Key=key,ExpiresIn=config.int["s3_link_expire_sec"])
    return response



    
    
        
        
  

