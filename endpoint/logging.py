
from setting import *
from utility import *
import json
import uuid

#1 logging create
async def logging_create(request):
   print(str(request.url))
   user_id = request.state.user_id
   #query set
    query="""insert into logging (created_by_id) values (:created_by_id) returning *;"""
    values={"created_by":user_id}
    #query run
    response=await database_execute(query,values)
