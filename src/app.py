#!/usr/bin/env python3
import time
import threading
import os
import datetime
import markovify
import re

from src.config import config
from src.ActivityPubTool import get_account_info, interact_activitypub_api, post_activity
from src.exportModel import generateAndExport


def worker():
    # 学習

    account_info = get_account_info(config)
    filename = "{}@{}".format(account_info["username"], config.domain)
    filepath = os.path.join("./chainfiles", os.path.basename(filename.lower()) + ".json")
    if os.path.isfile(filepath) and datetime.datetime.now().timestamp() - os.path.getmtime(filepath) < 60 * 60 * 24:
        print("モデルは再生成されません")
    else:
        generateAndExport(
            interact_activitypub_api(config, account_info['id']), filepath)
        print("LOG,GENMODEL," + str(datetime.datetime.now()) + "," + account_info["username"].lower())   # Log
    # 生成
    with open("./chainfiles/{}@{}.json".format(account_info["username"].lower(), config.domain)) as f:
        textModel = markovify.Text.from_json(f.read())
        sentence = textModel.make_sentence(tries=300)
        sentence = "".join(sentence.split()) + ' #bot'
        sentence = re.sub(r'(:.*?:)', r' \1 ', sentence)
        print(sentence)
    try:
        post_activity(config, sentence)
    except Exception as e:
        print("投稿エラー: {}".format(e))


def schedule(f, interval=1200, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


if __name__ == "__main__":
    # 定期実行部分
    schedule(worker)
    # worker()
