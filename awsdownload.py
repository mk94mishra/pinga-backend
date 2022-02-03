import boto3

s3 =boto3.client('s3',region_name="ap-south-1",aws_access_key_id="AKIA22OPN45JSL7EMXME",aws_secret_access_key="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")
s3.download_file('pingaweb-aps1', '7e389ca2-f364-4f53-8cc0-1a1856c9090b_1_mhiyu.jpeg', '7e389ca2-f364-4f53-8cc0-1a1856c9090b_1_mhiyu.jpeg')