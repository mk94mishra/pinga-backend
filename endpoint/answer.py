from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
import datetime
from enum import Enum, IntEnum
from typing import Optional

router=APIRouter(tags=["answer"])

#scehema
#1 answer
class answer(BaseModel):
   option_id:list
   scale:Optional[list]


#1 answer create
@router.post("/answer")
async def answer_create(request:Request,payload:answer):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #query set
   query="""insert into answer (created_by_id,option_id,data) values (:created_by_id,:option_id,:data) returning *"""
   # values={"created_by_id":user_id,"option_id":payload['option_id']}

   values_list = []
   i=0
   for o_id in payload['option_id']:
      scale = json.dumps({"scale":""})
      if payload['scale']:
         scale = json.dumps({"scale":payload['scale'][i]})
      i = i + 1
      values_list.append({"created_by_id": user_id, "option_id": o_id, "data":scale})
   values = values_list
   #query run
   response=await database_execute_many(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#2 answer read
@router.get("/answer/user/{user_id}/form/{form_id}")
async def answer_read(request:Request,user_id:int,form_id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""
   with
   q as (select * from question),
   o as (select * from "option")

   select 
   a.*,
   q.id as question_id, q.title as question_title, q.media_type as question_media_type, q.media_url as question_media_url, q.media_thumbnail_url as question_media_thumbnail_url,
   o.title as option_title,o.media_type as option_media_type, o.media_url as option_media_url, o.media_thumbnail_url as option_media_thumbnail_url, o.weightage as option_weightage 
   from answer as a 
   left join o on o.id=a.option_id
   left join q on q.id=o.question_id
   where q.form_id=:form_id and a.created_by_id=:user_id and a.flag is null
   """
   values={"form_id":form_id, "user_id":user_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   return response



#3 answer update
@router.put("/answer/{answer_id}/option/{option_id}")
async def answer_read(request:Request,answer_id:int,option_id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""update answer set option_id=:option_id where id=:answer_id and created_by_id=:user_id returning *"""
   values={"option_id":option_id,"answer_id":answer_id,"user_id":user_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   
   return response
   



#3 answer delete
@router.delete("/answer/user/{user_id}/form/{form_id}")
async def answer_read(request:Request,user_id:int,form_id:int):
   #prework
   # user_id=request.state.user_id
   #query set
   query="""with 
      q as (select * from question),
      o as (select * from "option")
      select ARRAY_AGG(a.id) as id
      from answer as a
      left join o on o.id=a.option_id
      left join q on q.id=o.question_id
      where a.created_by_id=:user_id and q.form_id=:form_id and a.flag is null"""
   values={"user_id":user_id,"form_id":form_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   print(response["message"])
   # array_list=response['id']
   array_list = response["message"][0]['id']
   #query set
   current_time = str(datetime.datetime.now())
   print(current_time)
   array_list = str(array_list).replace("[", "").replace("]", "")
   
   query="update answer set flag_date='"+current_time+"', flag='true' where id in ("+array_list+") and flag_date is null and flag is null"
   print(query)
   values={}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   
   return response
   


