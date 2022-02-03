# s3 upload
import boto3
import uuid
import requests
def get_presigned_url(filename_with_extension,user_id):
    #unique s3 key
    key=str(uuid.uuid4())+"_"+str(user_id)+"_"+filename_with_extension
    #s3 client
    s3_client=boto3.client('s3',region_name="ap-south-1",aws_access_key_id="AKIA22OPN45JSL7EMXME",aws_secret_access_key="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")
    #generate presigned post url
    response=s3_client.generate_presigned_post(Bucket="pinga-storage",Key=key,ExpiresIn=1000)
    print(response)
    #Upload file to S3 using presigned URL
    files = { 'file': open('myimage.jpeg', 'rb')}
    r = requests.post(response['url'], data=response['fields'], files=files)
    print(r)

    return response


get_presigned_url("myimage.jpeg",1)
# aws_access_key_id="AKIA22OPN45JSL7EMXME"
# aws_secret_access_key="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"
# aws_service="s3"
# region_name="ap-south-1"
# s3_bucket_name="pingaweb-aps1"
# s3_link_expire_sec=1000