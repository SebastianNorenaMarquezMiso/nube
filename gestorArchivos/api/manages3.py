import os
import boto3
import json
import io
from flask import Response
def upload_file(folder,file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    print("/////*****")
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_ID'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'))
    response = s3_client.upload_file(file_name, bucket, folder+"/"+file_name,ExtraArgs={'ACL': 'public-read'})
    return response


def download_file(folder,file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """

    s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_ID'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'))
    obj = s3.Object(bucket, folder+"/"+file_name)

    return  Response( obj.get()['Body'].read(), content_type='audio/mpeg')  
