from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["stock"])

#schema
class stock(BaseModel):
   assigned_to_id:int
   title:str
   given:int

#endpoint
#1 stock create
@router.post("/stock")
async def stock_create(request:Request,payload:stock):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #admin user check
   response = await is_admin(user_id)
   if response['status'] != "true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into stock (created_by_id,assigned_to_id,title,given,remaining) values (:created_by_id,:assigned_to_id,:title,:given,:remaining)"""
   values={"created_by_id":user_id,"assigned_to_id":payload['assigned_to_id'],"title":payload['title'],"given":payload['given'],"remaining":payload['given']}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 stock read all: self created
@router.get("/stock/self-created/")
async def stock_read_self_created(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from stock_master where created_by_id=:created_by_id limit 10 offset :offset;"""
   values={"created_by_id":user_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response

#3 stock delete: self created
@router.delete("/stock/{id}")
async def stock_delete(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #self user check
   query="""select created_by_id from stock where id=:id"""
   values={"id":id}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   stock=row[0]
   if stock['created_by_id']!=user_id:
      raise HTTPException(status_code=400,detail="not authorized")
   #query set
   query="""DELETE FROM stock WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

   
#4 stock read all: self assigned
@router.get("/stock/self-assigned/")
async def stock_read_self_assigned(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from stock_master where assigned_to_id=:assigned_to_id limit 10 offset :offset;"""
   values={"assigned_to_id":user_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#5 stock quantity change
@router.put("/stock/{id}/change-quantity")
async def stock_change_quantity(request:Request,id:int,remaining:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""update stock set remaining=:remaining where id=:id"""
   values={"id":id,"remaining":remaining}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
