from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["sex_o_scale"])


#scehema
#1 sex_o_scale
class sex_o_scale(BaseModel):
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
   query="""select * from mood where created_by_id=:created_by_id and created_at::date=:today"""
   values={"created_by_id":user_id,"today":today}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #mood assign
   mood=row
   #mood not exist
   if mood==[]:
      query="""insert into mood (created_by_id,data) values (:created_by_id,json_build_object('moodtype',:payload))"""
      values={"created_by_id":user_id, "payload":payload}
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

    
#2 mood read:self
@router.get("/mood/read-self-last-7-days")
async def mood_read_self_last_7_days(request:Request):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from mood where created_by_id=:created_by_id order by id desc limit 7;"""
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

  