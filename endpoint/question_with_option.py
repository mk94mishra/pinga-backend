from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum, IntEnum
import uuid

router=APIRouter(tags=["question"])


#validation
#1 media:type
class media_type(str, Enum):
    image='image'
    video='video'
    vector='vector'

#scehema
#1 question
class question(BaseModel):
   form_id:int
   title:str
   media_type:Optional[media_type]
   media_url:Optional[str] = None
   media_thumbnail_url:Optional[str] = None
   parent_question_id:Optional[int] = None
   parent_option_id:Optional[int] = None


#1 question create
@router.post("/question")
async def question_create(request:Request,payload:question):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response)
   
   unique_uuid = str(uuid.uuid1())
   #query set
   query="""insert into question (created_by_id,form_id,title,media_type,media_url,media_thumbnail_url,parent_question_id,parent_option_id,unique_uuid) values (:created_by_id,:form_id,:title,:media_type,:media_url,:media_thumbnail_url,:parent_question_id,:parent_option_id,:unique_uuid)"""
   values={"created_by_id":user_id,"form_id":payload['form_id'],"title":payload['title'],"media_type":payload['media_type'],"media_url":payload['media_url'],"media_thumbnail_url":payload['media_thumbnail_url'],"parent_question_id":payload['parent_question_id'],"parent_option_id":payload['parent_option_id'],"unique_uuid":unique_uuid}
   print(query, values)
   #query run
   await database_execute(query,values)

   #query set
   query="""select * from question where unique_uuid=:unique_uuid;"""
   values={"unique_uuid":unique_uuid}
   #query run
   response=await database_fetch_all(query,values)
   question_id = response['message'][0]['id']
   # insert options
   #query set
   query="""insert into option (created_by_id,question_id,title,media_type,media_url,media_thumbnail_url,unique_uuid) values (:created_by_id,:question_id,:title,:media_type,:media_url,:media_thumbnail_url,:unique_uuid)"""
   values=[{"created_by_id":user_id,"question_id":question_id,"title":payload['title'],"media_type":payload['media_type'],"media_url":payload['media_url'],"media_thumbnail_url":payload['media_thumbnail_url'],"unique_uuid":unique_uuid}
   ]
   #query run
   await database_execute_many(query,values)

   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 question read
@router.get("/question/form/{id}")
async def question_read(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from question where form_id=:form_id;"""
   values={"form_id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 question delete
@router.delete("/question/{id}")
async def question_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id

   #query set
   query="""DELETE FROM option WHERE question_id=:id"""
   values={"id":id}
   #query set
   query="""DELETE FROM question WHERE id=:id OR parent_question_id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)

   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response