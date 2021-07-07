import os
import pytest
from src.misskeyTool import get_account_info, fetch_notes, post_note, filter_contents


@pytest.fixture(scope="session")
def access_info() -> str:
    domain = os.environ.get("MISSKEY_TEST_DOMAIN")
    return domain


@pytest.fixture(scope="session")
def access_token() -> str:
    token = os.environ.get("MISSKEY_TEST_TOKEN")
    return token


@pytest.fixture(scope="module")
def account_id() -> str:
    account_id = os.environ.get("MISSKEY_TEST_ACCOUNT_ID")
    return account_id


def test_get_account_info(access_info, access_token, account_id):
    try:
        assert get_account_info(access_info, access_token).get('id') == account_id
    except Exception as e:
        pytest.fail(str(e))


def test_fetch_notes(access_info, access_token, account_id):
    param = {
        "limit": 10
    }
    try:
        assert fetch_notes(access_info, access_token, account_id, param)
    except Exception as e:
        pytest.fail(str(e))


def test_post_note(access_info, access_token):
    param = {
        "visibility": "home",
        "localOnly": True
    }
    try:
        assert post_note(access_info, access_token, "test", param)
    except Exception as e:
        pytest.fail(str(e))


def test_filter_true():
    # メンション文字
    assert filter_contents("論文も書かず研究もせず寝てる( @miwpayou0808@miwkey.miwpayou0808.info )") is True
    assert filter_contents("うんこ製造機(\n@miwpayou0808@miwkey.miwpayou0808.info )") is True
    # リンク
    assert filter_contents("https://github.com/mi-24v/mastodon-markov-bot/blob/main/src/app.py#L14 例えばこう") is True
    # 引用
    assert filter_contents("> ＞Storman氏が無職だと主張したため、約210万ドルもの賠償金は、今後3500年間、毎月50ドルずつ分割して支払われることになりました。\n🈚") is True

