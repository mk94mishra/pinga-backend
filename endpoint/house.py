from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["house"])

#scehema
#1 house
class house(BaseModel):
   mukhiya_name:str
   mukhiya_pic_url:str
   country:str
   state:str
   district:str
   village:str
   address:str
   member_count:int
   children_count:int
   pregnant_women_count:int
   sick_member_count:int
   at_patient_location:bool

#endpoint
#1 house create
@router.post("/house")
async def house_create(request:Request,payload:house):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   #query set
   query="""insert into house (created_by_id,data) values (:created_by_id,:data)"""
   values={"created_by_id":user_id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   

#2 house read all: self created
@router.get("/house/read-self-created/")
async def house_read_self_created(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from house_master where created_by_id=:created_by_id limit 10 offset :offset;"""
   values={"created_by_id":user_id,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#3 house read single
@router.get("/house/{id}")
async def house_read_single(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from house_master where id=:id;"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#4 house read all
@router.get("/house/read-all-admin/")
async def house_read_all_admin(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from house_master limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response
   

#4 house update
@router.put("/house/{id}")
async def house_update_self(request:Request,id:int,payload:house):
   #prework
   user_id = request.state.user_id
   payload=json.dumps(payload.dict())
   #query set
   query="""update house set data=:data where id=:id"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response 



#5 house delete
@router.delete("/house/{id}")
async def house_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""DELETE FROM house WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response