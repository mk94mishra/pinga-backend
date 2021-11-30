from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum, IntEnum
import uuid

router=APIRouter(tags=["health"])

#validation
#1 media:type
class type(str, Enum):
    period='period'

#scehema
#1 period
class period(BaseModel):
   start_date:Optional[date] = None
   end_date:Optional[date] = None



#1 period create
@router.post("/period")
async def period_create(request:Request,payload:period):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #query set
   query="""insert into health (created_by,start_date,end_date,type) values (:created_by,:start_date,:end_date,:type) returning *"""
   values={"created_by":user_id,"start_date":payload['start_date'],"end_date":payload['end_date'],"type":'period'}
   #query run
   response = await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

# put peried 
@router.put("/period/{period_id}")
async def period_update(request:Request,payload:period,period_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #query set
   query="""update health set start_date=:start_date, end_date=:end_date where id=:period_id and created_by=:created_by returning *"""
   values={"created_by":user_id,"start_date":payload['start_date'],"end_date":payload['end_date'],"type":'period',"period_id":period_id}
   #query run
   response = await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 health read
@router.get("/health/user/{user_id}")
async def health_read(request:Request,user_id:int,offset:int):
   
   #query set
   query="""select * from health where created_by=:created_by limit 30 offset :offset;"""
   values={"created_by":user_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 health delete
@router.delete("/health/{id}")
async def health_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   
   #query set
   query="""DELETE FROM health WHERE id=:id and created_by=:user_id"""
   values={"id":id,"user_id":user_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

