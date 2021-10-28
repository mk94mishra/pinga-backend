from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["member"])

#scehema
#1 house
class member_create(BaseModel):
   house_id:int
   gender:str
   name:str
   member_pic_url:Optional[str]
   relationship_mukhiya:str
   aadhar:str
   occupation:str
   total_children:int
   ongoing_medication:str
   medical_history:str
   past_operation:str
   last_menstrual_start:date
   last_menstrual_end:date
   last_doctor_visit:date
   dob:date
   is_married:bool
   has_miscarriage:bool
   has_allergy:bool


#2member update
class member_update(BaseModel):
   gender:str
   name:str
   member_pic_url:Optional[str]
   relationship_mukhiya:str
   aadhar:str
   occupation:str
   total_children:int
   ongoing_medication:str
   medical_history:str
   past_operation:str
   last_menstrual_start:date
   last_menstrual_end:date
   last_doctor_visit:date
   dob:date
   is_married:bool
   has_miscarriage:bool
   has_allergy:bool


#endpoint
#1 member create
@router.post("/member")
async def member_create(request:Request,payload:member_create):
   #prework
   payload=payload.dict()
   house_id=payload["house_id"]
   del payload["house_id"]
   user_id=request.state.user_id
   payload=json.dumps(payload,default=str)
   #query set
   query="""insert into member (created_by_id,house_id,data) values (:created_by_id,:house_id,:data)"""
   values={"created_by_id":user_id,"house_id":house_id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 member read all: self created
@router.get("/member/read-self-created/")
async def member_read_self_created(request:Request,offset:int):
   #prewrok
   user_id = request.state.user_id
   #query set
   query="""select * from member_master where created_by_id=:created_by_id limit 10 offset :offset;"""
   values={"created_by_id":user_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response

#3 house member read
@router.get("/member/house/{id}")
async def member_read_all_house(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from member where house_id=:house_id;"""
   values={"house_id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 member read single
@router.get("/member/{id}")
async def member_read_single(request:Request,id:int):
   #prewrok
   user_id = request.state.user_id
   #query set
   query="""select * from member_master where id=:id;"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#5 member read all
@router.get("/member/read-all-by-admin/")
async def member_read_all_by_admin(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from member_master limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#6 member read by form
@router.get("/member/form/{form_id}")
async def member_read_form(request:Request,form_id:int,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select a.form_id,  a.member_id , f.title as form_name,
      m.data->'name' as member_name
      from view_member_answer as a
      left join "member" as m on m.id=a.member_id
      left join form as f on f.id=a.form_id
      where a.form_id = :form_id
      group by a.member_id,a.form_id,m.data->'name',f.title 
      limit 10 offset :offset;"""
   values={"form_id":form_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#7 member update
@router.put("/member/{id}")
async def member_update_self(request:Request,id:int,payload:member_update):
   #prework
   user_id = request.state.user_id
   payload=json.dumps(payload.dict(),default=str)
   #query set
   query="""update member set data=:data where id=:id"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#8 member delete:self created
@router.delete("/member/{id}")
async def member_delete(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""DELETE FROM member WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
