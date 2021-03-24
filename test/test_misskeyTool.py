import os
import pytest
from src.misskeyTool import get_account_info, fetch_notes, post_note


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
        "text": "test",
        "localOnly": True
    }
    try:
        assert post_note(access_info, access_token, param)
    except Exception as e:
        pytest.fail(str(e))
