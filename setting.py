#1 env file load
from dotenv import dotenv_values
config = dotenv_values(".env")


#2 database object url
from databases import Database
database = Database('postgresql://{}:{}@{}:{}/{}'.format(config['db_user'],config['db_password'],config['db_host'],config['db_port'],config['db_name']))

#3 public endpoints
endpoint_public=[("GET",""),("GET","docs"),("GET","redoc"),("GET","openapi.json"),("POST","user/login-admin"),("POST","user/login-non-admin")]

