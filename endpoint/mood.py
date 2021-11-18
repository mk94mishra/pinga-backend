from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["mood"])


#scehema
#1 mood
class mood(BaseModel):
   type:list

#endpoint
#1 mood:create
@router.post("/mood")
async def mood_create(request:Request,payload:mood):
   #prework
   user_id = request.state.user_id
   payload=json.dumps(payload.dict()) 
   today=date.today()
   #mood get today of self user
   query="""select * from mood where created_by_id=:created_by_id and created_at::date=:today and type='mood'"""
   values={"created_by_id":user_id,"today":today}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #mood assign
   mood=row
   #mood not exist
   if mood==[]:
      query="""insert into mood (created_by_id,type,data) values (:created_by_id,:type,json_build_object('moodtype',:payload))"""
      values={"created_by_id":user_id,"type":'mood', "payload":payload}
      response=await database_execute(query,values)
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      return response
   #mood exist
   #query set
   query="""update mood set data=json_build_object('moodtype',:payload) where id=:id"""
   values={"payload":payload,"id":mood[0]["id"]}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#1 mood:sex o scale create
@router.post("/sex-o-scale")
async def sex_o_scale_create(request:Request,payload:mood):
   #prework
   user_id = request.state.user_id
   payload=json.dumps(payload.dict()) 
   today=date.today()
   #mood get today of self user
   query="""select * from mood where created_by_id=:created_by_id and created_at::date=:today and type=:type"""
   values={"created_by_id":user_id,"today":today,"type":type}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #mood assign
   mood=row
   #mood not exist
   if mood==[]:
      query="""insert into mood (created_by_id,type,data) values (:created_by_id,:type,json_build_object('sex_o_scale',:payload))"""
      values={"created_by_id":user_id,"type":'sex_o_scale', "payload":payload}
      response=await database_execute(query,values)
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      return response
   #mood exist
   #query set
   query="""update mood set data=json_build_object('sex_o_scale',:payload) where id=:id"""
   values={"payload":payload,"id":mood[0]["id"]}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#2 mood read:self
@router.get("/mood/read-self")
async def mood_read_self_last_7_days(request:Request):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from mood where created_by_id=:created_by_id order by id desc limit 15;"""
   values={"created_by_id":user_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#2 mood read all by type:by admin
@router.get("/mood/read-all-by-type")
async def mood_read_all_by_type(request:Request):
   #prework
   user_id = request.state.user_id
   # admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""select type, count(*) from mood group by type;"""
   values={}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response

  