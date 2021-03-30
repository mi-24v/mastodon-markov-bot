import requests
import sys


def get_account_info(domain: str, access_token: str):
    payload = {
        "i": access_token
    }
    res = requests.post("https://{}/api/i".format(domain), json=payload)
    if res.status_code != 200:
        print("アカウント情報のリクエストに失敗しました。", file=sys.stderr)
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
        print("ノートの取得リクエストに失敗しました。", file=sys.stderr)
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


def generate_fetched_notes(domain, access_token, account_id, params):
    raise NotImplementedError()  # TODO loadMastdonAPI相当のもの
