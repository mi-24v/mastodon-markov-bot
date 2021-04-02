import os
from enum import Enum, auto
from dotenv import load_dotenv
from yaml import load, CLoader


class ActivityPubSoftware(Enum):
    mastdon = auto()
    misskey = auto()
    pleroma = auto()  # 知らん
    unknown = auto()

    @classmethod
    def from_str(cls, name: str, *args):
        if name == "mastdon":
            return ActivityPubSoftware.mastdon
        elif name == "misskey":
            return ActivityPubSoftware.misskey
        elif name == "pleroma":
            return ActivityPubSoftware.pleroma
        else:
            return ActivityPubSoftware.unknown


class BotConfig:
    config_kv: dict
    domain: str
    read_access_token: str
    write_access_token: str
    activitypub_software: ActivityPubSoftware

    def __init__(self):
        with open("config.yaml") as f:
            self.config_kv = load(f, Loader=CLoader)

        self.activitypub_software = ActivityPubSoftware.from_str(self.config_kv["core"]["activitypub_software"])

        self.domain = os.environ.get('READ_DOMAIN')
        self.read_access_token = os.environ.get('READ_ACCESS_TOKEN')
        self.write_access_token = os.environ.get('WRITE_ACCESS_TOKEN')
        # dotenvから環境変数の読み込み(指定されていないとき)
        if self.domain is None or self.read_access_token is None or self.write_access_token is None:
            load_dotenv()
            self.domain = os.environ["READ_DOMAIN"]
            self.read_access_token = os.environ["READ_ACCESS_TOKEN"]
            self.write_access_token = os.environ["WRITE_ACCESS_TOKEN"]


config = BotConfig()
