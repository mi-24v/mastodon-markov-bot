#!/usr/bin/env python3
import time
import threading
import os
import datetime
import markovify
import re

from src.config import BotConfig
from src.ActivityPubTool import get_account_info, interact_activitypub_api, post_activity
from src.exportModel import generateAndExport


def worker(bot_config: BotConfig):
    # 学習

    account_info = get_account_info(bot_config)
    filename = "{}@{}".format(account_info["username"], bot_config.domain)
    dictionary_filepath = bot_config.dictionary_filepath
    if dictionary_filepath is None:
        dictionary_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                           "chainfiles",
                                           os.path.basename(filename.lower()) + ".json")
    # TODO lambdaで/tmp使いまわしのときにtimestampを無視する(falseは仮)
    if os.path.isfile(dictionary_filepath)\
            and datetime.datetime.now().timestamp() - os.path.getmtime(dictionary_filepath) < 60 * 60 * 24\
            and False:
        print("モデルは再生成されません")
    else:
        generateAndExport(
            interact_activitypub_api(bot_config, account_info['id']), dictionary_filepath)
        print("LOG,GENMODEL," + str(datetime.datetime.now()) + "," + account_info["username"].lower())   # Log
    # 生成
    with open(dictionary_filepath) as f:
        textModel = markovify.Text.from_json(f.read())
        sentence = textModel.make_sentence(tries=300)
        sentence = "".join(sentence.split()) + ' #bot'
        sentence = re.sub(r'(:.*?:)', r' \1 ', sentence)
        print(sentence)
    try:
        post_activity(bot_config, sentence)
    except Exception as e:
        print("投稿エラー: {}".format(e))


def schedule(f, interval=1200, wait=True, **kwargs):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f, kwargs=kwargs)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


if __name__ == "__main__":
    config = BotConfig.load()
    # 定期実行部分
    schedule(worker, bot_config=config)
    # worker()
