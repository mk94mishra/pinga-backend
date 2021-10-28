from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["issue"])

#validation
#1 issue:status
class issue_status(str, Enum):
    pending='pending'
    solved='solved'


#scehema
#1 issue
class issue(BaseModel):
   description:str
   media_url:str

#endpoint
#1 issue create
@router.post("/issue")
async def issue_create(request:Request,payload:issue):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #issue check
   if payload['description']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,media_url:any one is needed")
   #query set
   query="""insert into issue (created_by_id,description,media_url,status) values (:created_by_id,:description,:media_url,:status )"""
   values={"created_by_id":user_id,"description":payload['description'],"media_url":payload['media_url'],"status":"pending" }
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 issue read single
@router.get("/issue/{id}")
async def issue_read_single(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from issue_master where id=:id"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#3 issue read all pending:self created
@router.get("/issue/self-created-pending/")
async def issue_read_self_created_pending(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from issue_master where created_by_id=:created_by_id and status=:status limit 10 offset :offset;"""
   values={"created_by_id":user_id,"status":"pending","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   print("atur")
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#4 issue read all solved: self created
@router.get("/issue/self-created-solved/")
async def issue_read_self_created_solved(request:Request,offset:int):
   #prewrok
   user_id = request.state.user_id
   #query set
   query="""select * from issue_master where created_by_id=:created_by_id and status=:status limit 10 offset :offset;"""
   values={"created_by_id":user_id,"status":"solved","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#5 issue read all pending:admin
@router.get("/issue/admin-read-all-pending/")
async def issue_admin_read_all_pending(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from issue_master where status=:status limit 10 offset :offset;"""
   values={"status":"pending","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


@router.get("/issue/admin-read-all-solved/")
async def issue_admin_read_all_solved(request:Request,offset:int):
   #prewrok
   user_id = request.state.user_id
   # task get
   query="""select * from issue_master where status=:status limit 10 offset :offset;"""
   values={"status":"solved","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   
#6 issue mark solved
@router.put("/issue/{id}/mark-solved")
async def issue_mark_solved(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""update issue set status=:status where id=:id"""
   values={"status":"solved","id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   
#7 issue mark pending
@router.put("/issue/{id}/mark-pending")
async def issue_mark_pending(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""update issue set status=:status where id=:id"""
   values={"status":"pending","id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#8 issue delete
@router.delete("/issue/{id}")
async def issue_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""DELETE FROM issue WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response