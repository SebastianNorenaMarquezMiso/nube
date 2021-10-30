import boto3


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id='ASIA3I2TQPFIWOWZUU65',
    aws_secret_access_key='yWHmBEz6I5JBsxuHJE+U5scVwl5q2jExujoyStZx',
    aws_session_token='FwoGZXIvYXdzEFAaDG+RzJMYL31cSYczWiLKAelDTE2sBMeDthahPLi8JpK6FwOSESZTAFaX6GezhutXyqBOqbeiT1JPBUaZKmlFJ+UBo2HkBhC/Z/kWr2TBDzcfyORh2Btg1PEXPx+rzdsN7UNpOjQEMHH1bAG6+TDYOo3lIRELC1yoM2BByGoZ0eTkJnCKf2pAe+6lXcZMGnVH8xt3o4oc5llaHjyuZAIetR+WzTS/y8Vmnn3wzwwFFGPFRfJwDDaEvXnVriA7hBChMbB0L4ooHydR1bcfPdJ+XJxo2WvHCFP+I3Aokbr1iwYyLTdKD82GV49YtiNPv8tU3gUGYaBrhh2uRCIKsrcN9DlotqauC+An/uzjA3jOng==')
    response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
    return response


def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3', aws_access_key_id='ASIA3I2TQPFIWOWZUU65',
    aws_secret_access_key='yWHmBEz6I5JBsxuHJE+U5scVwl5q2jExujoyStZx',
    aws_session_token='FwoGZXIvYXdzEFAaDG+RzJMYL31cSYczWiLKAelDTE2sBMeDthahPLi8JpK6FwOSESZTAFaX6GezhutXyqBOqbeiT1JPBUaZKmlFJ+UBo2HkBhC/Z/kWr2TBDzcfyORh2Btg1PEXPx+rzdsN7UNpOjQEMHH1bAG6+TDYOo3lIRELC1yoM2BByGoZ0eTkJnCKf2pAe+6lXcZMGnVH8xt3o4oc5llaHjyuZAIetR+WzTS/y8Vmnn3wzwwFFGPFRfJwDDaEvXnVriA7hBChMbB0L4ooHydR1bcfPdJ+XJxo2WvHCFP+I3Aokbr1iwYyLTdKD82GV49YtiNPv8tU3gUGYaBrhh2uRCIKsrcN9DlotqauC+An/uzjA3jOng==')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    try:
        for item in s3.list_objects(Bucket=bucket)['Contents']:
            print(item)
            contents.append(item)
    except Exception as e:
        pass

    return contents