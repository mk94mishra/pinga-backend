from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["task"])

#validation
#1 task:status
class task_status(str, Enum):
    pending='pending'
    completed='completed'

#schema
#1 task
class task(BaseModel):
   assigned_to_id:int
   title:str
   description:list
   status:task_status

#endpoint
#1 task create
@router.post("/task/create-by-admin")
async def task_create_by_admin(request:Request,payload:task):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   # admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response) 
   #query set
   query="""insert into task (created_by_id, assigned_to_id, title, description, status) values (:created_by_id, :assigned_to_id, :title, :description, :status)"""
   values={"created_by_id":user_id, "assigned_to_id":payload['assigned_to_id'], "title":payload['title'], "description":payload['description'], "status":payload["status"]}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
 

#2 task delete
@router.delete("/task/{id}")
async def task_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #self user check
   query="""select created_by_id from task where id=:id"""
   values={"id":id}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   task=row[0]
   if task['created_by_id']!=user_id:
      raise HTTPException(status_code=400,detail="not authorized")
   #query set
   query="""DELETE FROM task WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

   
#3 task read single
@router.get("/task/{id}")
async def task_read_single(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from task_master where id=:id"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 task read all self created:pending
@router.get("/task/self-created-pending/")
async def task_read_self_created_pending(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from task_master where created_by_id=:created_by_id and status=:status limit 10 offset :offset;"""
   values={"created_by_id":user_id,"status":"pending","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#5 task read all self created:completed 
@router.get("/task/self-created-completed/")
async def task_read_self_created_completed(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from task_master where created_by_id=:created_by_id and status=:status limit 10 offset :offset;"""
   values={"created_by_id":user_id,"status":"completed","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#6 task read all self assigned:pending 
@router.get("/task/self-assigned-pending/")
async def task_read_self_assigned_pending(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from task_master where assigned_to_id=:assigned_to_id and status=:status limit 10 offset :offset;"""
   values={"assigned_to_id":user_id,"status":"pending","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#7 task read all self assigned:completed
@router.get("/task/self-assigned-completed/")
async def task_read_self_assigned_completed(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from task_master where assigned_to_id=:assigned_to_id and status=:status limit 10 offset :offset;"""
   values={"assigned_to_id":user_id,"status":"completed","offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#8 task mark completed
@router.put("/task/{id}/mark-completed")
async def task_update_mark_completed(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""update task set status=:status where id=:id"""
   values={"status":"completed","id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#9 task mark pending
@router.put("/task/{id}/mark-pending")
async def task_update_mark_pending(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""update task set status=:status where id=:id"""
   values={"status":"pending","id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
