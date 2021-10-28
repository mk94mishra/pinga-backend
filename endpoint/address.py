from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *

router=APIRouter(tags=["address"])

#1 country read
@router.get("/address/country")
async def country_read_all(request:Request):
   #query set
   query="""select * from address where type=:type;"""
   values={"type":'country'}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#2 country read single
@router.get("/address/country/{id}")
async def country_read_single(request:Request,id:int):
   #query set
   query="""select * from address where id=:id;"""
   values={"id":'id'}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#3 state read
@router.get("/address/state/country/{country_id}")
async def state_read_all(request:Request,country_id:int):
   #query set
   query="""select * from address where type=:type and parent_address_id=:country_id;"""
   values={"type":'state',"country_id":country_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#4 state read single
@router.get("/address/state/{id}")
async def state_read_single(request:Request,id:int):
   #query set
   query="""select * from address where type=:type and id=:id;"""
   values={"type":'state',"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#5 district read
@router.get("/address/district/state/{state_id}")
async def district_read_all(request:Request,state_id:int):
   #query set
   query="""select * from address where type=:type and parent_address_id=:state_id;"""
   values={"type":'district',"state_id":state_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#6 district read single
@router.get("/address/district/{id}")
async def district_read_single(request:Request,id:int):
   #query set
   query="""select * from address where type=:type and id=:id;"""
   values={"type":'district',"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#7 town/city/village read
@router.get("/address/town/district/{district_id}")
async def town_read_all(request:Request,district_id:int):
   #query set
   query="""select * from address where type=:type and parent_address_id=:district_id;"""
   values={"type":'town',"district_id":district_id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#8 town/city/village read single
@router.get("/address/town/{id}")
async def town_read_single(request:Request,id:int):
   #query set
   query="""select * from address where type=:type and id=:id;"""
   values={"type":'town',"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response