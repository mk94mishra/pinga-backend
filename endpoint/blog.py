from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["blog"])

#validation
#1 media:type
class media_type(str, Enum):
    image='image'
    video='video'
    pdf='pdf'
    empty=''


#schema
#1 blog
class blog(BaseModel):
   title:str
   data: str
   link_url:str
   media_type:media_type
   media_thumbnail_url:str
   media_url:str
   type:str
   day:str


#endpoint
#1 blog create
@router.post("/blog")
async def blog_create(request:Request,payload:blog):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #payload check
   if payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,link_url,media_url:any one is needed")
   #query set
   query="""insert into blog (created_by_id,description,link_url,media_type,media_thumbnail_url,media_url,type,day) values (:created_by_id,:description,:link_url,:media_type,:media_thumbnail_url,:media_url,:type,:day) returning *"""
   values={"created_by_id":user_id,"description":payload['description'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"type":payload['type'],"day":payload['day']}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   
#3 blog read:by all
@router.get("/blog/")
async def blog_read(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from blog limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#3 blog read:by type
@router.get("/blog/type/{blog_type}")
async def blog_read_type(request:Request,blog_type:str):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from blog where type=:blog_type ;"""
   values={"blog_type":blog_type}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 blog delete
@router.delete("/blog/{id}")
async def blog_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #self user check
   query="""select * from blog where id=:id"""
   values={"id":id}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   post=row[0]
   if post['created_by_id']!=user_id:
      raise HTTPException(status_code=400,detail="not authorized")   
   #query set
   query="""DELETE FROM blog WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   
