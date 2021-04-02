from src import misskeyTool
from src import mastdonTool
from src.config import BotConfig, ActivityPubSoftware


class NotImplementedException(Exception):
    pass


def get_account_info(config: BotConfig):
    if config.activitypub_software == ActivityPubSoftware.mastdon:
        return mastdonTool.get_account_info(config.domain, config.read_access_token)
    elif config.activitypub_software == ActivityPubSoftware.misskey:
        return misskeyTool.get_account_info(config.domain, config.read_access_token)
    else:
        raise NotImplementedException("unknown software")


def post_activity(config: BotConfig, content: str):
    if config.activitypub_software == ActivityPubSoftware.mastdon:
        param = config.config_kv["write_mastdon"].copy()
        param.update({"status": content})
        return mastdonTool.post_toot(config.domain,
                                     config.write_access_token,
                                     param)
    elif config.activitypub_software == ActivityPubSoftware.misskey:
        return misskeyTool.post_note(config.domain,
                                     config.write_access_token,
                                     content,
                                     config.config_kv["write_misskey"].copy())
    else:
        raise NotImplementedException("unknown software")


def fetch_activities(config: BotConfig, account_id: str):
    if config.activitypub_software == ActivityPubSoftware.mastdon:
        return mastdonTool.fetchToots(config.domain,
                                      config.read_access_token,
                                      account_id,
                                      config.config_kv["read_mastdon"])
    elif config.activitypub_software == ActivityPubSoftware.misskey:
        return misskeyTool.fetch_notes(config.domain,
                                       config.read_access_token,
                                       account_id,
                                       config.config_kv["read_misskey"].copy())
    else:
        raise NotImplementedException("unknown software")


def interact_activitypub_api(config: BotConfig, account_id: str):
    activities: str
    if config.activitypub_software == ActivityPubSoftware.mastdon:
        activities = mastdonTool.loadMastodonAPI(config.domain,
                                                 config.read_access_token,
                                                 account_id,
                                                 config.config_kv["read_mastdon"])
    elif config.activitypub_software == ActivityPubSoftware.misskey:
        activities = misskeyTool.generate_fetched_notes(config.domain,
                                                        config.read_access_token,
                                                        account_id,
                                                        config.config_kv["read_misskey"].copy(),
                                                        config.config_kv["core"]["source_activity_count"])
    else:
        raise NotImplementedException("unknown software")
    return activities
