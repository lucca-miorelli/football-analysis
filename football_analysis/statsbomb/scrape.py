import json
from dataclasses import dataclass

import boto3
from botocore.client import BaseClient
from mypy_boto3_s3 import ServiceResource
from mypy_boto3_s3.service_resource import Bucket

from football_analysis.config import cc


@dataclass
class AWS:
    def __post_init__(self):
        self.client: BaseClient = boto3.client(
            "s3",
            aws_access_key_id=cc.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=cc.AWS_SECRET_ACCESS_KEY,
            region_name=cc.AWS_DEFAULT_REGION,
            endpoint_url=cc.AWS_ENDPOINT_URL,
        )
        self.resource: ServiceResource = boto3.resource(
            "s3",
            aws_access_key_id=cc.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=cc.AWS_SECRET_ACCESS_KEY,
            region_name=cc.AWS_DEFAULT_REGION,
            endpoint_url=cc.AWS_ENDPOINT_URL,
        )
        self.bucket: Bucket = self.resource.Bucket(cc.AWS_BUCKET_NAME)

    def save_to_json(self, data: dict, path: str, file_name: str):
        self.client.put_object(
            Body=json.dumps(data),
            Bucket=cc.AWS_BUCKET_NAME,
            Key=f"{path}/{file_name}.json",
        )
