from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from typing import Optional

router=APIRouter(tags=["issue"])


#scehema
#1 subscribe
class subscribe(BaseModel):
   type:str
   email:Optional[str]=None
   mobile:Optional[str]=None

#endpoint
#1 subscribe create
@router.post("/subscribe")
async def subscribe_create(request:Request,payload:subscribe):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #issue check
   if payload['email']=='' and payload['mobile']=='':
      raise HTTPException(status_code=400,detail="email,mobile:any one is needed")
   #query set
   query="""insert into subscribe (created_by_id,email,mobile,type) values (:created_by_id,:email,:mobile,:type)"""
   values={"created_by_id":user_id,"email":payload['email'],"mobile":payload['mobile'],"type":payload['type'] }
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 subscribe read single
@router.get("/subscribe")
async def subscribe_read_user(request:Request):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from subscribe where created_by_id=:user_id"""
   values={"user_id":user_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#3 subscribe read all pending:self created
@router.get("/subscribe/all")
async def subscribe_all(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from subscribe limit 100 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   
