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
   payload=payload.dict()
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
   mood_data = json.dumps({'moodtype':payload['type']})
   if mood==[]:
      query="""insert into mood (created_by_id,type,data) values (:created_by_id,:type,:mood_data)"""
      values={"created_by_id":user_id,"type":'mood', "mood_data":mood_data}
      response=await database_execute(query,values)
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      return response
   #mood exist
   #query set
   query="""update mood set data=:mood_data where id=:id"""
   values={"mood_data":mood_data,"id":mood[0]["id"]}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#1 mood:sex o scale create
@router.post("/mood/sex-o-scale")
async def sex_o_scale_create(request:Request,payload:mood):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   sex_scale_data = json.dumps({'sex_o_scale':payload['type']})
   today=date.today()
   #mood get today of self user
   query="""select * from mood where created_by_id=:created_by_id and created_at::date=:today and type=:type"""
   values={"created_by_id":user_id,"today":today,"type":'sex_o_scale'}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #mood assign
   mood=row
   #mood not exist
   if mood==[]:
      query="""insert into mood (created_by_id,type,data) values (:created_by_id,:type,:sex_scale_data)"""
      values={"created_by_id":user_id,"type":'sex_o_scale', "sex_scale_data":sex_scale_data}
      response=await database_execute(query,values)
      if response["status"]=="false":
         raise HTTPException(status_code=400,detail=response)
      return response
   #mood exist
   #query set
   query="""update mood set data=:sex_scale_data where id=:id"""
   values={"sex_scale_data":sex_scale_data,"id":mood[0]["id"]}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#2 mood read:self
@router.get("/mood/read-self")
async def mood_read_self(request:Request):
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

  