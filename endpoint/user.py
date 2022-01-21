from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from enum import Enum, IntEnum
import random
import uuid
from sms import *

router=APIRouter(tags=["user"])

#validation
#1 user:type
class user_type(str, Enum):
    admin='admin'
    worker='worker'
    fellow="fellow"
    user="user"
#2 gender
class gender(str, Enum):
   cis_female='Cis female'
   cis_male='Cis male'
   gender_expansive='Gender expansive'
   intersex='Intersex'
   non_binary='Non binary'
   trans_female='Trans female'
   trans_male='Trans male'
   prefer_not_to_say='Prefer not to say'
  

#scehema
#1 user:login
class user_login(BaseModel):
   mobile:str
   password:str
class user_login_google_auth(BaseModel):
   google_auth:str
   email:Optional[str]=None

class user_login_mobile_otp_auth(BaseModel):
   mobile:str
   otp:Optional[str]=None

class verify_reset_login_otp(BaseModel):
   otp:str
   password:str
   email:Optional[str]=None
   mobile:Optional[str]=None
class reset_login_otp(BaseModel):
   email:Optional[str]=None
   mobile:Optional[str]=None

#2 user update:profile
class user_profile(BaseModel):
   name:str
   email:str
   gender:gender
   dob:date
   profile_pic_url:str
   height:str
   weight:str
   tnc_accepted:bool
#3 user:create
class user_create(BaseModel):
   type:user_type
   mobile:str
   password:str
#4 extra:interest
class interest(BaseModel):
   interest:list

#endpoint
#1 user login:admin
@router.post("/user/login-admin")
async def user_login_admin(request:Request,payload:user_login):
   #prework
   payload=payload.dict()   
   payload['password'] = password_hash_create(payload['password'])
   #query set
   query="""select * from "user" where mobile=:mobile and password=:password"""
   values={"mobile":payload['mobile'],"password":payload['password']}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #pick user
   user=row[0]
   #admin check
   if user['type']!="admin":
      raise HTTPException(status_code=400,detail="you are not an admin")
   #token create 
   token = token_create(user['id'])
   #finally
   if user['name']==None:
      response = {'id':user['id'],'token': token,'next endpoint':"profile update"}
      return response
   response = {'id':user['id'],'token': token,'next':"admin app homepage"}
   return response


#2 user login:non admin
@router.post("/user/login-non-admin")
async def user_login_non_admin(request:Request,payload:user_login):
   #prework
   payload=payload.dict()   
   payload['password'] = password_hash_create(payload['password'])
   #query set
   query="""select * from "user" where mobile=:mobile and password=:password"""
   values={"mobile":payload['mobile'],"password":payload['password']}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #pick first element
   print(response["message"])
   if response["message"] == []:
      response["status"]=="false"
      response = {'status':"false",'message': "wrong credentials"}
      raise HTTPException(status_code=400,detail=response)
   user=row[0]
  
   #token create 
   token = token_create(user['id'])
   #finally
   if user['name']==None:
      response = {'id':user['id'],'token': token,'next endpoint':"profile update"}
      return response
   response = {'id':user['id'],'token': token,'next':"app homepage"}
   return response



#2 user login:otp mobile non admin
@router.post("/user/login-mobile-otp")
async def user_login_mobile_otp_auth_non_admin(request:Request,payload:user_login_mobile_otp_auth):
   #prework
   payload=payload.dict()   
   #query set
   query="""select id, mobile, name from "user" where mobile=:mobile and is_active='true'"""
   values={"mobile":payload['mobile']}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   if response["message"] == []:
      response["status"]=="false"
      response = {'status':"false",'message': "mobile number not exist!"}
      raise HTTPException(status_code=400,detail=response)
   #pick first element
   user=row[0]

   #query set
   query="""select  AGE(NOW(),created_at)::text AS difference  from otp where mobile=:mobile and otp=:otp order by id desc limit 1"""
   values={"mobile":payload['mobile'],"otp":payload['otp']}
   #query run
   response=await database_fetch_all(query,values)
   if response["message"] == []:
      response = {"status":"false", "message":"otp not verified!"}
      raise HTTPException(status_code=400,detail=response)
   
   diffrence = response["message"][0]['difference'].split(':')
   if int(diffrence[1])>=5:
      response = {"status":"false", "message":"otp expired!"}
      raise HTTPException(status_code=400,detail=response)

   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)

   
   #token create 
   token = token_create(user['id'])
   #finally
   if user['name']==None:
      response = {'id':user['id'],'token': token,'next endpoint':"profile update"}
      return response
   response = {'id':user['id'],'token': token,'next':"app homepage"}
   return response



#2 user login:non admin
@router.post("/user/login-non-admin-google")
async def user_login_non_admin(request:Request,payload:user_login_google_auth):
   #prework
   payload=payload.dict()   
   #query set
   query="""select * from "user" where google_auth=:google_auth and email=:email"""
   values={"google_auth":payload['google_auth'],"email":payload['email']}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #pick first element
   if response["message"] == []:
      response["status"]=="false"
      response = {'status':"false",'message': "wrong credentials"}
      raise HTTPException(status_code=400,detail=response)
   user=row[0]
   #admin check
   # if user['type']=="admin":
   #    raise HTTPException(status_code=400,detail="you are an admin")
   #token create 
   token = token_create(user['id'])
   #finally
   if user['name']==None:
      response = {'id':user['id'],'token': token,'next endpoint':"profile update"}
      return response
   response = {'id':user['id'],'token': token,'next':"app homepage"}
   return response



#3 user profile update:self
@router.put("/user/profile-update-self")
async def user_update_profile_self(request:Request,payload:user_profile):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()   
   #query set
   query="""update "user" set name=:name,email=:email,gender=:gender,dob=:dob,profile_pic_url=:profile_pic_url,weight=:weight,height=:height,tnc_accepted=:tnc_accepted where id=:id"""
   values={"name":payload['name'],"email":payload['email'],"gender":payload['gender'],"dob":payload['dob'], "profile_pic_url":payload['profile_pic_url'],"weight":payload['weight'],"height":payload['height'],"tnc_accepted":payload["tnc_accepted"],"id":user_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#3 user profile update:self
@router.put("/user/profile-update-self/interest")
async def user_update_profile_self_interest(request:Request,payload:interest):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   interest_data =json.dumps(payload)
   #query set
   query="""update "user" set data=:interest_data where id=:id"""
   values={"interest_data":interest_data,"id":user_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#5 user login info update:self
@router.put("/user/login-info-update-self")
async def user_update__login_info_self(request:Request,payload:user_login):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #both is needed check
   if payload['mobile']=="" or payload["password"]=="":
      raise HTTPException(status_code=400,detail="key can't be none")
   payload["password"]=password_hash_create(payload['password'])
   #query set
   query="""update "user" set mobile=:mobile,password=:password where id=:id"""
   values={"mobile":payload["mobile"],"password":payload["password"],"id":user_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#4 user read:self
@router.get("/user/read-self")
async def user_read_self(request:Request):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from "user" where id=:id"""
   values={"id":user_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"][0]
   if row['password']:
      row['password'] = "already set"
   else:
      row['password'] = "not set"
   #finally
   response=row
   return response


#6 user read all: by admin
@router.get("/user/read-all-by-admin/")
async def user_read_all_by_admin(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   # admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""select * from "user" order by created_at desc limit 10 offset :offset"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response

#7 user create: by admin
@router.post("/user/create-by-admin")
async def user_create_by_admin(request:Request,payload:user_create):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   password_hash=password_hash_create(payload['password'])
   # admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response) 
   #query set
   query="""insert into "user" (mobile,password,type,created_by) values (:mobile,:password,:type,:created_by)"""
   values={"mobile":payload['mobile'],"password":password_hash,"type":payload['type'],"created_by":user_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   

#8 user read single by admin
@router.get("/user/{id}")
async def user_get_single(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from "user" where id=:id"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response 
  

  
#9 user search by mobile: by admin
@router.get("/user/search-by-mobile/")
async def user_search_by_mobile(request:Request,mobile:str):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from "user" where mobile=:mobile"""
   values={"mobile":mobile}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#10 user create: by self
@router.post("/user/signup-normal")
async def public_user_signup_normal(request:Request,payload:user_login):
   #prework
   payload=payload.dict()
   payload["mobile"]=payload["mobile"].lower()
   payload["password"]=hashlib.md5(payload['password'].encode()).hexdigest()
   #check null value
   if '' in list(payload.values()) or any(' ' in ele for ele in list(payload.values())):
      raise HTTPException(status_code=400,detail="null or white space not allowed")
   
   #query set
   query="""insert into "user" (created_by,type,mobile,password) values (:created_by,:type,:mobile,:password) returning *;"""
   values={"created_by":1,"type":"normal","mobile":payload['mobile'],"password":payload['password']}
   #query run
   response=await database_execute(query,values)
   #query fail
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   response["next"]="login-non-admin"
   return response
   


#10 user create: by self
@router.post("/user/signup-google")
async def public_user_signup_google(request:Request,payload:user_login_google_auth):
   #prework
   payload=payload.dict()
   #check null value
   if '' in list(payload.values()) or any(' ' in ele for ele in list(payload.values())):
      raise HTTPException(status_code=400,detail="null or white space not allowed")
   mobile = str(uuid.uuid1()) + "test"
   password = str(random.randrange(20, 50, 3)) + "test"
   print(mobile)
   #query set
   query="""insert into "user" (created_by,type,mobile,password,google_auth,email) values (:created_by,:type,:mobile,:password,:google_auth,:email) returning *;"""
   values={"created_by":1,"type":"normal","mobile":mobile,"password":password,"google_auth":payload['google_auth'],"email":payload['email']}
   #query run
   response=await database_execute(query,values)
   #query fail
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   response["next"]="login-non-admin-google-auth"
   return response


@router.post("/user/create-login-otp")
async def user_login_create(request:Request,payload:user_login_mobile_otp_auth):
   #prework
   payload=payload.dict()
   
   new_otp = str(random.randint(1111,9999))
   sms_text = 'PINGA login OTP is '+new_otp
   try:

      #query set
      query="""select * from "user" where mobile=:mobile"""
      values={"mobile":payload['mobile']}
      #query run
      response=await database_fetch_all(query,values)
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      row=response["message"]
      #pick first element
      if response["message"] == []:
         response["status"]=="false"
         response = {'status':"false",'message': "Mobile Number Not Exist!"}
         raise HTTPException(status_code=400,detail=response)

      sms_response=sendSMS(payload['mobile'], sms_text)
      sms_response=dict(json.loads(sms_response.decode()))
      print(sms_response)
      if sms_response['status'] != 'success':
         response = {"status":"failed", "message":"otp not sent!"}
         raise HTTPException(status_code=400,detail=response)
      #query set
      query="""insert into otp (mobile,otp) values (:mobile,:otp);"""
      values={"mobile":payload['mobile'],"otp":new_otp}
      #query run
      print("response")
      response=await database_execute(query,values)
      #query fail
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      #finally
      response = {"status":"success", "message":"otp sent!","next":"login-mobile-otp"}
      return response
   except:
      response = {"status":"false", "message":"otp not sent!"}
      raise HTTPException(status_code=400,detail=response)
   


@router.post("/user/create-password-reset-otp")
async def user_password_reset_create(request:Request,payload:reset_login_otp):
   #prework
   payload=payload.dict()
   
   new_otp = str(random.randint(1111,9999))
   sms_text = "OTP for PINGA password reset is "+new_otp+". Do not share it with anyone."
   try:
      sms_response=sendSMS(payload['mobile'], sms_text)
      sms_response=dict(json.loads(sms_response.decode()))
      if sms_response['status'] != 'success':
         response = {"status":"failed", "message":"otp not sent!"}
         raise HTTPException(status_code=400,detail=response)
      #query set
      query="""insert into otp (mobile,email,otp) values (:mobile,:email,:otp);"""
      values={"mobile":payload['mobile'],"email":payload['email'],"otp":new_otp}
      #query run
      response=await database_execute(query,values)
      #query fail
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      #finally
      response = {"status":"success", "message":"otp sent!","next":"verify-password-reset-otp"}
      return response
   except:
      response = {"status":"false", "message":"otp not sent!"}
      raise HTTPException(status_code=400,detail=response)
   


@router.post("/user/verify-password-reset-otp")
async def user_password_reset_create(request:Request,payload:verify_reset_login_otp):
   #prework
   payload=payload.dict()
   #query set
   query="""select  AGE(NOW(),created_at)::text AS difference  from otp where mobile=:mobile and otp=:otp order by id desc limit 1"""
   values={"mobile":payload['mobile'],"otp":payload['otp']}
   
   #query run
   response=await database_fetch_all(query,values)

   if response["message"] == []:
      response = {"status":"false", "message":"otp not verified!"}
      raise HTTPException(status_code=400,detail=response)
   
   diffrence = response["message"][0]['difference'].split(':')
   if int(diffrence[1])>=50:
      response = {"status":"false", "message":"otp expired!"}
      raise HTTPException(status_code=400,detail=response)

   password_hash=password_hash_create(payload['password'])
   query="""update "user" set password=:password where mobile=:mobile"""
   values={"password":password_hash,"mobile":payload['mobile']}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   response = {"status":"success", "message":"password reset succesfully!"}
   return response
