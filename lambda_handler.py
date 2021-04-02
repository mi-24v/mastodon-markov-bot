import os
import boto3
from src.app import worker


def lambda_handler(event, context):
    os.environ["READ_DOMAIN"] = fetch_ssm_parm("mastdon-markov-bot.read_domain")
    os.environ["READ_ACCESS_TOKEN"] = fetch_ssm_parm("mastdon-markov-bot.read_access_token")
    os.environ["WRITE_ACCESS_TOKEN"] = fetch_ssm_parm("mastdon-markov-bot.write_access_key")
    worker()


def fetch_ssm_parm(param_key: str) -> str:
    ssm = boto3.client("ssm")
    res = ssm.get_parameter(Name=param_key, WithDecryption=True)
    return res["Parameter"]["Value"]
