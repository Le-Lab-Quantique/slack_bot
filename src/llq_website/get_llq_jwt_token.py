from typing import Literal

import requests

from .exceptions import NoLLQJWTTokenException
from .utils import base_url

from config import Config

BearerToken = Literal["Bearer"]


def _get_credentials() -> dict[str, str]:
    return {
        "username": Config.LLQ_USERNAME,
        "password": Config.LLQ_PASSWORD,
    }


def get_token() -> BearerToken:
    url = f"{base_url}/wp-json/jwt-auth/v1/token"
    response = requests.post(
        url,
        json=_get_credentials(),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        token = response.json()["token"]
        return f"Bearer {token}"
    else:
        username = _get_credentials()["username"]
        raise NoLLQJWTTokenException(
            f"Failed to get LLQ JWT Token for {username}. \nStatus code : {response.status_code}"
        )
