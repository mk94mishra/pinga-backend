from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum, IntEnum
import json

router=APIRouter(tags=["extra"])

#validation
#1 extra:type
class extra_type(str, Enum):
   quickguide='quick-guide'
   scheme='scheme'
   helpdesk='helpdesk'
   interest='interest'
   mood='mood'
   admin='admin'
   pingasm_result='pingasm_result'
   motivation='motivation'
   typeform='typeform'
   web='web'

#scehema
#1 extra:quick-guide
class quick_guide(BaseModel):
   title:str
   description:str
   link_url:str
   media_url:str


#1 extra:mood
class mood(BaseModel):
   moodtype:list
 
#2 extra:scheme
class scheme(BaseModel):
   title:str
   description:str
   link_url:str
   media_url:str

#3 extra:helpdesk
class helpdesk(BaseModel):
   name:str
   mobile:str
   whatsapp:str


#4 extra:interest
class interest(BaseModel):
   title:str
   media_url:Optional[str]=None


#5 extra:admin
class admin(BaseModel):
   data:dict

#5 extra:typeform
class typeform(BaseModel):
   event_id:Optional[str]=None
   event_type:Optional[str]=None
   form_response:dict

#5 extra:readtypeform
class readtypeform(BaseModel):
   typeform_id:int

#5 extra:motivation
class motivation(BaseModel):
   data:dict

#5 extra:web
class web(BaseModel):
   data:dict

#endpoint
#1 extra create:quickguide
@router.post("/extra/quick-guide")
async def extra_create_quickguide(request:Request,payload:quick_guide):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data)"""
   values={"created_by_id":user_id,"type":"quick-guide","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 extra create:scheme
@router.post("/extra/scheme")
async def extra_create_scheme(request:Request,payload:scheme):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data)"""
   values={"created_by_id":user_id,"type":"scheme","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

#2 extra create:mood
@router.post("/extra/mood")
async def extra_create_mood(request:Request,payload:mood):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=401,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data)"""
   values={"created_by_id":user_id,"type":"mood","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#3 extra create:helpdesk
@router.post("/extra/helpdesk")
async def extra_create_helpdesk(request:Request,payload:helpdesk):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data)"""
   values={"created_by_id":user_id,"type":"helpdesk","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


# extra create:interest
@router.post("/extra/interest")
async def extra_create_interest(request:Request,payload:interest):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data)"""
   values={"created_by_id":user_id,"type":"interest","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response




#3 extra create:admin
@router.post("/extra/admin")
async def extra_create_admin(request:Request,payload:admin):
   #prework
   user_id=request.state.user_id
   payload=payload.dict()
   payload=json.dumps(payload['data'])
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data) returning *"""
   values={"created_by_id":user_id,"type":"admin","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#3 extra create:admin
@router.post("/extra/typeform")
async def extra_create_typeform(request:Request,payload:typeform):
   #prework
   # user_id=request.state.user_id
   payload=payload.dict()
   payload['data']  = {'event_id':payload['event_id'], 'event_type':payload['event_type'],'form_response':payload['form_response']}
   payload=json.dumps(payload['data'])
   
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data) returning *"""
   values={"created_by_id":1,"type":"typeform","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#4 extra create:motivation
@router.post("/extra/motivation")
async def extra_create_motivation(request:Request,payload:motivation):
   #prework
   user_id=request.state.user_id
   payload=payload.dict()
   payload=json.dumps(payload['data'])
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data) returning *"""
   values={"created_by_id":user_id,"type":"motivation","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#2 extra create:web
@router.post("/extra/web")
async def extra_create_web(request:Request,payload:web):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   # admin user check
   response = await is_admin(user_id)
   if response['status']!="true":
      raise HTTPException(status_code=400,detail=response)
   #query set
   query="""insert into extra (created_by_id,type,data) values (:created_by_id,:type,:data) returning *"""
   values={"created_by_id":user_id,"type":"web","data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#4 extra read single
@router.get("/extra/{id}/read-single")
async def extra_read_single(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from extra_master where id=:id ;"""
   values={"id":id}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response



#4 extra read typeform
@router.post("/extra/read-typeform")
async def extra_read_single_typeform(request:Request,payload:readtypeform):
   payload=payload.dict()
   #query set
   query="""select * from extra where id=:id and type='typeform';"""
   values={"id":payload['typeform_id']}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#5 extra read all
@router.get("/extra/{type}/read-all/")
async def extra_read_all(request:Request,type:extra_type,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from extra where type=:type limit 10 offset :offset;"""
   values={"type":type,"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#5 extra read all
@router.get("/extra/web/read-all")
async def extra_web_read_all(request:Request):
   
   #query set
   query="""select * from extra where type='web'"""
   values={}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response


#6 extra update
@router.put("/extra/{id}/quick-guide")
async def extra_update_quick_guide(request:Request,id:int,payload:quick_guide):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   #query set
   query="""update extra set data=:data where id=:id"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#7 extra update
@router.put("/extra/{id}/helpdesk")
async def extra_update_helpdesk(request:Request,id:int,payload:helpdesk):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   #query set
   query="""update extra set data=:data where id=:id"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#7 extra update
@router.put("/extra/{id}/interest")
async def extra_update_interest(request:Request,id:int,payload:interest):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   #query set
   query="""update extra set data=:data where id=:id"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#8 extra update
@router.put("/extra/{id}/scheme")
async def extra_update_scheme(request:Request,id:int,payload:scheme):
   #prework
   user_id=request.state.user_id
   payload=json.dumps(payload.dict())
   #query set
   query="""update extra set data=:data where id=:id"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#6 extra update
@router.put("/extra/{id}/admin")
async def extra_update_admin(request:Request,id:int,payload:admin):
   #prework
   user_id=request.state.user_id
   payload=payload.dict()
   payload = json.dumps(payload['data'])
   #query set
   query="""update extra set data=:data where id=:id returning *"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response

#6 extra update
@router.put("/extra/{id}/web")
async def extra_update_web(request:Request,id:int,payload:web):
   #prework
   user_id=request.state.user_id
   payload=payload.dict()
   payload = json.dumps(payload)
   #query set
   query="""update extra set data=:data where id=:id returning *"""
   values={"id":id,"data":payload}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response



#9 extra:delete
@router.delete("/extra/{id}")
async def extra_delete(request:Request,id:int):
   #prework
   user_id=request.state.user_id
   #query set
   query="""DELETE FROM extra WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


#10 get presigned-url
@router.get("/extra/get-presigned-url/{filename_with_extension}")
async def get_s3_presigned_url(request:Request,filename_with_extension:str):
   #prework
   user_id=request.state.user_id
   # query set
   response=await get_presigned_url(filename_with_extension,user_id)
   #fianlly
   return response

