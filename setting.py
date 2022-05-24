#1 env file load
from dotenv import dotenv_values
config = dotenv_values(".env")

min_size=5
max_size=10

#2 database object url
from databases import Database
database = Database('postgresql://{}:{}@{}:{}/{}'.format(config['db_user'],config['db_password'],config['db_host'],config['db_port'],config['db_name']),min_size=5,max_size=30)

#3 public endpoints
endpoint_public=[("GET",""),("GET","docs"),("GET","redoc"),("GET","openapi.json"),("POST","user/login-admin"),("POST","user/login-non-admin"),("POST","user/signup-normal"),("POST","user/login-non-admin-google"),("POST","user/signup-google"),("POST","user/create-password-reset-otp"),("POST","user/verify-password-reset-otp"),("POST","user/create-login-otp"),("POST","user/login-mobile-otp"),("GET","result/test"),("POST","extra/typeform"),("POST","extra/read-typeform"),("GET","mylocal"),("GET","extra/web/read-all")]

