from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["post"])

#validation
#1 media:type
class media_type(str, Enum):
    image='image'
    video='video'
    pdf='pdf'
    empty=''


#schema
#1 post
class post(BaseModel):
   description:str
   link_url:str
   media_type:media_type
   media_thumbnail_url:str
   media_url:str


#endpoint
#1 post create
@router.post("/post")
async def post_create(request:Request,payload:post):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #payload check
   if payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,link_url,media_url:any one is needed")
   #query set
   query="""insert into post (created_by_id,description,link_url,media_type,media_thumbnail_url,media_url) values (:created_by_id,:description,:link_url,:media_type,:media_thumbnail_url,:media_url)"""
   values={"created_by_id":user_id,"description":payload['description'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url']}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   
#5 like create:by all
@router.put("/post/{id}/like-create")
async def post_like_create(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""update post set like_count=like_count + 1 where id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
  

#3 post read:by all
@router.get("/post/")
async def post_read(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from post_master limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 post delete
@router.delete("/post/{id}")
async def post_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #self user check
   query="""select * from post where id=:id"""
   values={"id":id}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   post=row[0]
   if post['created_by_id']!=user_id:
      raise HTTPException(status_code=400,detail="not authorized")   
   #query set
   query="""DELETE FROM post WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   

#5 post search by user:type
@router.get("/post/search-by-user-type/")
async def post_search_user_type(request:Request,user_type:str):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from post_master where created_by_user_type=:user_type limit 10 offset :offset ;"""
   values={"user_type":user_type}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#6 my post
@router.get("/post/self/")
async def post_self(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from post_master where created_by_id=:created_by_id limit 10 offset :offset ;"""
   values={"created_by_id":user_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response