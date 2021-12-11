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
   score: Optional[int] = 0
   weightage: Optional[int] = 0
   media_type:Optional[media_type]
   media_url:Optional[str] = None
   media_thumbnail_url:Optional[str] = None
   parent_question_id:Optional[int] = 0
   parent_option_id:Optional[int] = 0
   


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
   query="""insert into question (created_by_id,form_id,title,media_type,media_url,media_thumbnail_url,parent_question_id,parent_option_id,score,weightage,unique_uuid) values (:created_by_id,:form_id,:title,:media_type,:media_url,:media_thumbnail_url,:parent_question_id,:parent_option_id,:score,:weightage,:unique_uuid)"""
   values={"created_by_id":user_id,"form_id":payload['form_id'],"title":payload['title'],"media_type":payload['media_type'],"media_url":payload['media_url'],"media_thumbnail_url":payload['media_thumbnail_url'],"parent_question_id":payload['parent_question_id'],"parent_option_id":payload['parent_option_id'],"score":payload['score'],"weightage":payload['weightage'],"unique_uuid":unique_uuid}
   
   #query run
   response = await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)

   #query set
   query="""select * from question where unique_uuid=:unique_uuid;"""
   values={"unique_uuid":unique_uuid}
   #query run
   response=await database_fetch_all(query,values)

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
   query="""with
         q1 as (select q.*, 
         ARRAY_AGG(o.id) as option_id, ARRAY_AGG(o.title) as option_title, ARRAY_AGG(o.media_type) as option_media_type, ARRAY_AGG(o.media_url) as option_media_url, ARRAY_AGG(o.media_thumbnail_url) as option_media_thumbnail_url
         from question as q
         left join option as o on o.question_id=q.id
         where q.parent_question_id is null and q.parent_option_id is null and q.form_id=:form_id
         group by q.id)

         select q.*,
         ARRAY_AGG(o.id) as option_id, ARRAY_AGG(o.title) as option_title, ARRAY_AGG(o.media_type) as option_media_type, ARRAY_AGG(o.media_url) as option_media_url, ARRAY_AGG(o.media_thumbnail_url) as option_media_thumbnail_url
         from question as q
         left join option as o on o.question_id=q.id
         left join q1 on q1.id = q.parent_question_id
         where q.form_id=:form_id
         group by q1.id,q.id
         order by q.id asc;"""
   values={"form_id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



# question update
@router.put("/question/{question_id}")
async def question_put(request:Request,payload:question,question_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response)
   
   #query set
   query="""update question set title=:title, media_type=:media_type, media_url=:media_url,media_thumbnail_url=:media_thumbnail_url,parent_question_id=:parent_question_id,parent_option_id=:parent_option_id,score=:score,weightage=:weightage where id=:question_id"""
   values={"title":payload['title'],"media_type":payload['media_type'],"media_url":payload['media_url'],"media_thumbnail_url":payload['media_thumbnail_url'],"parent_question_id":payload['parent_question_id'],"parent_option_id":payload['parent_option_id'],"score":payload['score'],"weightage":payload['weightage'],"question_id":question_id}
   
   #query run
   response = await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)

   #finally
   return response


#4 question delete
@router.delete("/question/{id}")
async def question_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id


   #query set
   query="""DELETE FROM option WHERE question_id=:id"""
   values={"id":id}
   await database_execute(query,values)
   
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