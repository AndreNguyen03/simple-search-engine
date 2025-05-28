import os
import boto3
import json
from botocore.exceptions import ClientError

def load_db_password_from_aws(secret_name, region_name="us-east-1"):
    client = boto3.client('secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error getting secret: {e}")
        raise e

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
        password = secret_dict.get("password")
        if password:
            os.environ['PG_PASSWORD'] = password
        else:
            raise Exception("Password not found in secret")
    else:
        raise Exception("SecretString not found in secret")

if __name__ == "__main__":
    # Gọi hàm này trước khi import config
    load_db_password_from_aws(secret_name="myapp/db-password", region_name="us-east-1")
