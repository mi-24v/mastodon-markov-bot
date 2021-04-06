import os
import boto3
from pathlib import PurePath
import botocore.exceptions
from src.app import worker
from src.config import BotConfig


def lambda_handler(event, context):
    config: BotConfig = BotConfig.load()
    dictionary_path = config.dictionary_filepath
    if dictionary_path is None:
        raise ValueError("dictionary path must be specified")
    access_between_local_and_s3(dictionary_path, "download")
    config.domain = fetch_ssm_parm("mastdon-markov-bot.read_domain")
    config.read_access_token = fetch_ssm_parm("mastdon-markov-bot.read_access_token")
    config.write_access_token = fetch_ssm_parm("mastdon-markov-bot.write_access_key")
    worker(config)
    access_between_local_and_s3(dictionary_path, "upload")


def access_between_local_and_s3(local_path: str, mode: str):
    bucket_name = os.environ["S3_BUCKET"]
    s3 = boto3.resource("s3")
    filename = PurePath(local_path).name
    if mode == "upload":
        s3.meta.client.upload_file(local_path, bucket_name, filename)
    elif mode == "download":
        try:
            s3.Object(bucket_name, filename).load()
            s3.meta.client.download_file(bucket_name, filename, local_path)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return
            else:
                raise e
    else:
        raise ValueError("mode string should be 'upload' or 'download'")


def fetch_ssm_parm(param_key: str) -> str:
    ssm = boto3.client("ssm")
    res = ssm.get_parameter(Name=param_key, WithDecryption=True)
    return res["Parameter"]["Value"]
