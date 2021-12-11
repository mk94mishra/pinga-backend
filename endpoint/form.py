from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["form"])


#validation
#1 form:language
class language(str, Enum):
    marathi='marathi'
    hindi='hindi'
    english='english'
    swahili='swahili'

#scehema
#1 form
class form(BaseModel):
   title:str
   description:Optional[str] = None
   media_url:Optional[str] = None
   language:Optional[language]
   type:Optional[str] = None
   next:Optional[str] = None
   

#endpoint
#1 form create
@router.post("/form")
async def form_create(request:Request,payload:form):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #title is needed check
   if payload['title']=="":
      raise HTTPException(status_code=400,detail="title can't be none")
   #admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query sey
   query="""insert into form (created_by_id,title,description,media_url,language, type, next) values (:created_by_id,:title,:description,:media_url,:language,:type,:next)"""
   values={"created_by_id":user_id,"title":payload['title'],"description":payload['description'],"media_url":payload['media_url'],"language":payload['language'],"type":payload['type'],"next":payload['next']}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 form read single
@router.get("/form/{id}")
async def form_read_single(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from form where id=:id"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#3 form read language all
@router.get("/form/language/{language}")
async def form_read_language(request:Request,language:str,offset:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from form where is_active=true and language =:language limit 10 offset :offset;"""
   values={"language":language,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#4 form read all
@router.get("/form")
async def form_read_all(request:Request,offset:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from form where is_active=true and type='form' limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#4 form read all games
@router.get("/form/game")
async def form_game_read_all(request:Request,offset:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""select * from form where is_active=true and type='game' limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#5 form update
@router.put("/form/{id}")
async def form_update(request:Request,id:int,payload:form):
   #prework
   user_id=request.state.user_id
   payload=payload.dict()
   #title is needed check
   if payload['title']=="":
      raise HTTPException(status_code=400,detail="title can't be none")
   #query set
   query="""update form set title=:title,description=:description,media_url=:media_url where id=:id"""
   values={"id":id,"title":payload['title'],"description":payload['description'],"media_url":payload['media_url']}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   

#6 form delete
@router.delete("/form/{id}")
async def form_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""DELETE FROM form WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
 
