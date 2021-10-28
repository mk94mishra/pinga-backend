from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *

router=APIRouter(tags=["monitor"])


@router.get("/monitor/{date}")
async def monitor_fellow_report(request:Request,date:str):
   date = date+'%'
   #query set
   query="""with
      a as (select distinct created_by_id,  count(distinct member_id) as total_member
      from "answer" where created_at::text like :created_at
      group by created_by_id)

      select u.name, a.*
      from a 
      left join "user" as u on u.id=a.created_by_id"""
   values={"created_at":date}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response

