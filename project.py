#1 fastapi project
from fastapi import FastAPI
project = FastAPI(title = "pinga backend", version = "1.0")


#4 cors middleware add
from fastapi.middleware.cors import CORSMiddleware
#from starlette.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
project.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
print({"message":"cors middleware added"})


#2 project root end point
from fastapi import Request
from setting import config
#define root endpoint
@project.get("/")
async def root(request:Request):   
   response={"endpoint":"root","host":request.headers.get("host"),"project":config['project_name']}
   return response


#3 router add
from router import *


#5 middleware request check
from utility import *
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
@project.middleware("http")
async def middleware_request_check(request:Request,endpoint_function):
   print({"message":"middleware started","endpoint":request.url})

   # public endpoint check
   response = await is_public_endpoint(request)
   if response['status']=="true":
      response=await endpoint_function(request)
      return response

   #private endpoint check
   response = await has_valid_token(request)
   if response['status']=="true":
      request.state.user_id=response['message']["user_id"]
      response=await endpoint_function(request)
      return response

   return JSONResponse(status_code=400, content=jsonable_encoder(response))



#6  database connect startup event
from setting import database
#3 startup event
@project.on_event("startup")
async def db_connect():
   await database.connect()
   print({"message":"database connected"})


#7  database disconnect startup event
@project.on_event("shutdown")
async def db_disconnect():
   await database.disconnect()
   print({"message":"disconnected from database"})
