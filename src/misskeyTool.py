import requests
import sys
import re
from logging import getLogger

logger = getLogger(__name__)


def get_account_info(domain: str, access_token: str):
    payload = {
        "i": access_token
    }
    res = requests.post("https://{}/api/i".format(domain), json=payload)
    if res.status_code != 200:
        logger.error("アカウント情報のリクエストに失敗しました。")
        res.raise_for_status()
    return res.json()


def fetch_notes(domain: str, access_token: str, account_id: str, params: dict):
    payload = {
        "i": access_token,
        "userId": account_id
    }
    payload.update(params)
    res = requests.post("https://{}/api/users/notes".format(domain), json=payload)
    if res.status_code != 200:
        logger.error("ノートの取得リクエストに失敗しました。")
        res.raise_for_status()
    return res.json()


def post_note(domain: str, access_token: str, content: str, params: dict):
    payload = {
        "i": access_token,
        "text": content
    }
    payload.update(params)
    res = requests.post("https://{}/api/notes/create".format(domain), json=payload)
    if res.status_code != 200:
        print("ノートの投稿に失敗しました。", file=sys.stderr)
        res.raise_for_status()
    return res.json()


def filter_contents(content_text: str) -> bool:
    # メンション文字(@)から始まる単語かリンクを含むときマッチ
    search_hits = re.search(r"@\w|https?://", content_text)
    return False if search_hits is None else True


def fetch_notes_loop(domain: str, access_token: str, account_id: str, params: dict, loop_count: int):
    notes = []
    for _ in range(loop_count):
        try:
            fetched_notes = fetch_notes(domain, access_token, account_id, params)
            for note in fetched_notes:
                last_read_id = note["id"]
                text = note["text"]
                if note["visibility"] == "followers" or note["visibility"] == "specified":
                    logger.info("プライベート投稿のためスキップ: {}".format(text))
                    continue
                elif filter_contents(text):
                    logger.info("フィルタにヒットしたためスキップ: {}".format(text))
                    continue
                else:
                    logger.info("[note] {}".format(text))
                    notes.append(text)
                params["untilId"] = last_read_id
        except Exception as e:
            logger.error("Error: {}".format(e))
            break
    # 重複投稿を削除
    result_notes = list(set(notes))
    return result_notes


def generate_fetched_notes(domain: str, access_token: str, account_id: str, params: dict, loop_size: int):
    notes = fetch_notes_loop(domain, access_token, account_id, params, loop_size)
    return "\n".join(notes)
