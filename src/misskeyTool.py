import requests


def get_account_info(domain: str, access_token: str):
    payload = {
        "i": access_token
    }
    res = requests.post("https://{}/api/i".format(domain), data=payload)
    if res.status_code != 200:
        raise Exception("アカウント情報のリクエストに失敗しました。")
    return res


def fetch_notes(domain: str, access_token: str, account_id: str, params: dict):
    payload = {
        "i": access_token,
        "userId": account_id
    } | params
    res = requests.post("https://{}/api/users/notes".format(domain), data=payload)
    if res.status_code != 200:
        raise Exception("ノートの取得リクエストに失敗しました。")
    return res


def post_note(domain: str, access_token: str, params: dict):
    payload = {
        "i": access_token
    } | params
    res = requests.post("https://{}/api/notes/create".format(domain), data=payload)
    if res.status_code != 200:
        raise Exception("ノートの投稿に失敗しました。")
    return res

