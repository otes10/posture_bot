from dotenv import load_dotenv
import boto3

import os

##Initialize the s3 bot
def initialize():
    load_dotenv()
    AWSUSER_SECRET = os.environ.get('AWSUSER_SECRET')
    AWSUSER_ID = os.environ.get('AWSUSER_ID')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    return boto3.client('s3',
                    'us-west-1',
                    aws_access_key_id= AWSUSER_ID,
                    aws_secret_access_key= AWSUSER_SECRET
                     )


### file needs to be binary so file.get_contents(binary=True), and name is just how you want to name the file in the bucket
def upload_file(file, name):
    s3 = initialize()
    load_dotenv()
    s3.put_object(Body=file,
                      Bucket=os.environ.get('AWS_BUCKET_NAME'),
                      Key= name,
                      ContentType='text/plain')
    
### below are used for downloads, files are chuncked if too large
def get_total_bytes(name):
    s3 = initialize()
    load_dotenv()
    result = s3.list_objects(Bucket=os.environ.get('AWS_BUCKET_NAME'))
    for item in result['Contents']:
        if item['Key'] == name :
            return item['Size']


def get_object(total_bytes, name):
    s3 = initialize()
    load_dotenv()
    if total_bytes > 1000000:
        return get_object_range(total_bytes, name)
    return s3.get_object(Bucket= os.environ.get('AWS_BUCKET_NAME'), Key=name)['Body'].read()


def get_object_range(total_bytes, name):
    s3 = initialize()
    load_dotenv()
    offset = 0
    while total_bytes > 0:
        end = offset + 999999 if total_bytes > 1000000 else ""
        total_bytes -= 1000000
        byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
        offset = end + 1 if not isinstance(end, str) else None
        yield s3.get_object(Bucket= os.environ.get('AWS_BUCKET_NAME'), Key=name, Range=byte_range)['Body'].read()

