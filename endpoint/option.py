from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum, IntEnum
import uuid

router=APIRouter(tags=["option"])

#validation
#1 media:type
class media_type(str, Enum):
    image='image'
    video='video'
    vector='vector'

#scehema
#1 option
class option(BaseModel):
   question_id:int
   title:Optional[str] = None
   media_type:Optional[media_type]
   media_url:Optional[str] = None
   media_thumbnail_url:Optional[str] = None
   weightage:int



#1 option create
@router.post("/option")
async def option_create(request:Request,payload:option):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response)
   
   unique_uuid = str(uuid.uuid1())
   #query set
   query="""insert into option (created_by_id,question_id,title,media_type,media_url,media_thumbnail_url,weightage,unique_uuid) values (:created_by_id,:question_id,:title,:media_type,:media_url,:media_thumbnail_url,:weightage,:unique_uuid)"""
   values={"created_by_id":user_id,"question_id":payload['question_id'],"title":payload['title'],"media_type":payload['media_type'],"media_url":payload['media_url'],"media_thumbnail_url":payload['media_thumbnail_url'],"weightage":payload['weightage'],"unique_uuid":unique_uuid}
   #query run
   response = await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""select * from option where unique_uuid=:unique_uuid;"""
   values={"unique_uuid":unique_uuid}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 option read
@router.get("/option/question/{id}")
async def option_read(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from option where question_id=:question_id;"""
   values={"question_id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 option delete
@router.delete("/option/{id}")
async def option_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   
   #query set
   query="""DELETE FROM option WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

