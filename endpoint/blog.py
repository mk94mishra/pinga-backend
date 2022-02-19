from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum
from typing import Optional, List

router=APIRouter(tags=["blog"])

#validation
#1 media:type
class media_type(str, Enum):
    image='image'
    video='video'
    pdf='pdf'
    empty=''


#schema
#1 blog: period
class period(BaseModel):
   title:str
   description: str
   link_url:Optional[str]=None
   media_type:Optional[str]=None
   media_thumbnail_url:Optional[str]=None
   media_url:Optional[str]=None
   day:int


#2 blog: collection
class collection(BaseModel):
   title:str
   collection: str
   course_name:str
   description:str
   link_url:Optional[str]=None
   media_type:Optional[str]=None
   media_thumbnail_url:Optional[str]=None
   media_url:Optional[str]=None
   day:Optional[int]=None


#2 blog: collection_category
class collection_category(BaseModel):
   category:Optional[str]=None
   course_name:Optional[str]=None


#endpoint
#1 blog period create
@router.post("/blog/period")
async def period_create(request:Request,payload:period):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   blog_type = 'period'
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""insert into blog (created_by_id,title,link_url,media_type,media_thumbnail_url,media_url,type,day,data) values (:created_by_id,:title,:link_url,:media_type,:media_thumbnail_url,:media_url,:type,:day,:data) returning *"""
   values={"created_by_id":user_id,"title":payload['title'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"type":blog_type,"day":payload['day'],"data":description}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   



# blog : harmonometer create
@router.post("/blog/harmonometer")
async def harmonometer_create(request:Request,payload:period):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   blog_type = 'harmonometer'
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""insert into blog (created_by_id,title,link_url,media_type,media_thumbnail_url,media_url,type,day,data) values (:created_by_id,:title,:link_url,:media_type,:media_thumbnail_url,:media_url,:type,:day,:data) returning *"""
   values={"created_by_id":user_id,"title":payload['title'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"type":blog_type,"day":payload['day'],"data":description}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   

   

# blog : moodometer create
@router.post("/blog/moodometer")
async def moodometer_create(request:Request,payload:period):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   blog_type = 'moodometer'   
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""insert into blog (created_by_id,title,link_url,media_type,media_thumbnail_url,media_url,type,day,data) values (:created_by_id,:title,:link_url,:media_type,:media_thumbnail_url,:media_url,:type,:day,:data) returning *"""
   values={"created_by_id":user_id,"title":payload['title'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"type":blog_type,"day":payload['day'],"data":description}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   

   

# blog : sexoscale create
@router.post("/blog/sexoscale")
async def sexoscale_create(request:Request,payload:period):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   blog_type = 'sex_o_scale'
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""insert into blog (created_by_id,title,link_url,media_type,media_thumbnail_url,media_url,type,day,data) values (:created_by_id,:title,:link_url,:media_type,:media_thumbnail_url,:media_url,:type,:day,:data) returning *"""
   values={"created_by_id":user_id,"title":payload['title'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"type":blog_type,"day":payload['day'],"data":description}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   



#2 blog collection create
@router.post("/blog/collection")
async def collection_create(request:Request,payload:collection):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   blog_type = 'collection'
   #payload check
   if payload['title']=='' and payload['collection']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="collection,link_url,media_url:any one is needed")

   json_data = json.dumps({'collection':payload['collection'],'description':payload['description'],'course_name':payload['course_name']})
   #query set
   query="""insert into blog (created_by_id,title,link_url,media_type,media_thumbnail_url,media_url,type,day,data) values (:created_by_id,:title,:link_url,:media_type,:media_thumbnail_url,:media_url,:type,:day,:data) returning *"""
   values={"created_by_id":user_id,"title":payload['title'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"type":blog_type,"day":payload['day'],"data":json_data}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response 
   


# update blog: period
@router.put("/blog/period/{blog_id}")
async def blog_period_update(request:Request,payload:period,blog_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="title,description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""update blog set title=:title, link_url=:link_url,media_type=:media_type,media_thumbnail_url=:media_thumbnail_url,media_url=:media_url,data=:description,day=:day where id=:blog_id returning *"""
   values={"title":payload['title'],"description":description,"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"day":payload['day'],"blog_id":blog_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


# update blog: harmonometer
@router.put("/blog/hormonometer/{blog_id}")
async def blog_hormonometer_update(request:Request,payload:period,blog_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="title,description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""update blog set title=:title, link_url=:link_url,media_type=:media_type,media_thumbnail_url=:media_thumbnail_url,media_url=:media_url,data=:description,day=:day where id=:blog_id returning *"""
   values={"title":payload['title'],"description":description,"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"day":payload['day'],"blog_id":blog_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response




# update blog: moodometer
@router.put("/blog/moodometer/{blog_id}")
async def blog_moodometer_update(request:Request,payload:period,blog_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="title,description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""update blog set title=:title, link_url=:link_url,media_type=:media_type,media_thumbnail_url=:media_thumbnail_url,media_url=:media_url,data=:description,day=:day where id=:blog_id returning *"""
   values={"title":payload['title'],"description":description,"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"day":payload['day'],"blog_id":blog_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response





# update blog: sexoscale
@router.put("/blog/sexoscale/{blog_id}")
async def blog_sexoscale_update(request:Request,payload:period,blog_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   
   #payload check
   if payload['title']=='' and payload['description']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="title,description,link_url,media_url:any one is needed")

   description = json.dumps({'description':payload['description']})
   #query set
   query="""update blog set title=:title, link_url=:link_url,media_type=:media_type,media_thumbnail_url=:media_thumbnail_url,media_url=:media_url,data=:description,day=:day where id=:blog_id returning *"""
   values={"title":payload['title'],"description":description,"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"day":payload['day'],"blog_id":blog_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response


# update blog: collection
@router.put("/blog/collection/{blog_id}")
async def blog_collection_update(request:Request,payload:collection,blog_id:int):
   #prework
   user_id = request.state.user_id
   payload=payload.dict()
   #payload check
   if payload['title']=='' and payload['collection']=='' and payload['link_url']=='' and payload['media_url']=='':
      raise HTTPException(status_code=400,detail="collection,link_url,media_url:any one is needed")

   json_data = json.dumps({'collection':payload['collection'],'description':payload['description'],'course_name':payload['course_name']})
   #query set
   query="""update blog set title=:title,link_url=:link_url,media_type=:media_type,media_thumbnail_url=:media_thumbnail_url,media_url=:media_url,day=:day,data=:data where id=:blog_id returning *"""
   values={"title":payload['title'],"link_url":payload['link_url'],"media_type":payload['media_type'],"media_thumbnail_url":payload['media_thumbnail_url'],"media_url":payload['media_url'],"day":payload['day'],"data":json_data, 'blog_id':blog_id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   


#3 blog read:by all
@router.get("/blog")
async def blog_read(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from blog limit 10 offset :offset;"""
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response




#3 blog read:by collection
@router.post("/blog/collection/read")
async def blog_read_collection(request:Request,offset:int,payload:collection_category):
   payload=payload.dict()
   #query set
   query="select * from blog where data->>'collection'::text like '%"+payload['category']+"%' and data->>'course_name'::text like '%"+payload['course_name']+"%' limit 10 offset :offset;"
   print(query)
   values={"offset":offset}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]

   #finally
   response=row
   return response




#3 blog read:by collection category with cousre name
@router.post("/blog/collection-category-course-name")
async def blog_read_collection_category_coursename(request:Request,offset:int,payload:collection_category):   
   payload=payload.dict()
   #query set
   query="""select data->'collection' as category, data->'course_name' as course_name from blog 
   where type='collection' and data->>'collection'!=''
   group by data->'collection', data->'course_name' limit 100 offset :offset;"""
   values={"offset":offset}
   if payload['category']:
      #query set
      query="select data->'collection' as category, data->'course_name' as course_name from blog where type='collection' and data->>'collection'::text like '%"+payload['category']+"%' group by data->'collection', data->'course_name' limit 100 offset :offset;"
      values={"offset":offset}
   print(query)
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response





#3 blog read:by collection-list
@router.get("/blog/collection-list")
async def blog_read_collection_category(request:Request,offset:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select ARRAY_AGG(interest::text) as collection_list from view_collection_list limit 200 offset :offset;"""
   values={"offset":offset}
   print(query)
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response




#3 blog read:by type
@router.get("/blog/type/{blog_type}")
async def blog_read_type(request:Request,blog_type:str):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from blog where type=:blog_type ;"""
   values={"blog_type":blog_type}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response




#3 blog read:by day
@router.get("/blog/day/{day}")
async def blog_read_day(request:Request,day:int):
   #prework
   user_id = request.state.user_id
   #query set
   query="""select * from blog where day=:day ;"""
   values={"day":day}
   #query run
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   #finally
   response=row
   return response




#4 blog delete
@router.delete("/blog/{id}")
async def blog_delete(request:Request,id:int):
   #prework
   user_id = request.state.user_id
   #self user check
   query="""select * from blog where id=:id"""
   values={"id":id}
   response=await database_fetch_all(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   row=response["message"]
   post=row[0]
   if post['created_by_id']!=user_id:
      raise HTTPException(status_code=400,detail="not authorized")   
   #query set
   query="""DELETE FROM blog WHERE id=:id"""
   values={"id":id}
   #query run
   response=await database_execute(query,values)
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   #finally
   return response
   
