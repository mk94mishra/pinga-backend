from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from typing import Optional

router=APIRouter(tags=["mylocal"])


#scehema
#1 subscribe
class subscribe(BaseModel):
   type:str
   email:Optional[str]=None
   mobile:Optional[str]=None
   notification:Optional[list]

#endpoint
#1 subscribe create


sql_data = [
   {'day':1,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(82).png'},
{'day':2,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(83).png'},
{'day':4,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(84).png'},
{'day':5,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(85).png'},
{'day':6,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(86).png'},
{'day':7,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(87).png'},
{'day':8,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(88).png'},
{'day':9,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(89).png'},
{'day':10,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(90).png'},
{'day':11,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(91).png'},
{'day':12,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(92).png'},
{'day':13,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(93).png'},
{'day':14,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(94).png'},
{'day':15,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(95).png'},
{'day':16,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(96).png'},
{'day':17,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(97).png'},
{'day':18,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(98).png'},
{'day':19,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(99).png'},
{'day':20,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(100).png'},
{'day':21,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(101).png'},
{'day':22,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(102).png'},
{'day':23,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(103).png'},
{'day':24,'link':'https://pinga-storage.s3.ap-south-1.amazonaws.com/blog/Screenshot+(104).png'}
]
# @router.get("/mylocal")
# async def mylocal_create(request:Request):
   
#    for x in sql_data:
#       print(x['day'],x['link'])
#       #query set
#       query="""update blog set media_type='image',media_url=:media_url where type='hormonometer' and day=:day"""
#       values={"day":x['day'],"media_url":x['link']}
#       #query run
#       response=await database_execute(query,values)
#       print(response)
#       if response["status"]=="false":
#          raise HTTPException(status_code=400,detail=response)

#    return "rest"




@router.get("/mylocal")
async def mylocal_create(request:Request):
   import emails
   message = emails.html(html="<p>Hi!<br>Here is your receipt...",
                           subject="Your receipt No. 567098123",
                           mail_from=('Some Store', 'manish@pingaweb.com'))


   r = message.send(to='mk94mishra@gmail.com', smtp={'host': 'pingaweb.com', 'timeout': 5})
   print(r)

   return r

