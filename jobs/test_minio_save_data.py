import json
import logging
from dataclasses import dataclass
import os

from football_analysis.config import cc

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from mypy_boto3_s3 import ServiceResource
from mypy_boto3_s3.service_resource import Bucket


# Read data from data folder as json
with open(os.path.join('data', 'matches', '9', '281.json'), 'r') as f:
    data = json.load(f)

client: BaseClient = boto3.client(
    "s3",
    aws_access_key_id=cc.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=cc.AWS_SECRET_ACCESS_KEY,
    region_name=cc.AWS_DEFAULT_REGION,
    endpoint_url=cc.AWS_ENDPOINT_URL,
)
resource: ServiceResource = boto3.resource(
    "s3",
    aws_access_key_id=cc.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=cc.AWS_SECRET_ACCESS_KEY,
    region_name=cc.AWS_DEFAULT_REGION,
    endpoint_url=cc.AWS_ENDPOINT_URL,
)
bucket: Bucket = resource.Bucket(cc.AWS_BUCKET_NAME)

# Put object
client.put_object(
    Body=json.dumps(data),
    Bucket=cc.AWS_BUCKET_NAME,
    Key='matches/9/281.json'
)