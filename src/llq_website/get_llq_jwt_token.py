import os
from typing import Literal

import requests

from .exceptions import NoLLQJWTTokenException
from .utils import base_url

BearerToken = Literal["Bearer"]


def _get_credentials() -> dict[str, str]:
    return {
        "username": os.environ.get("LLQ_USERNAME"),
        "password": os.environ.get("LLQ_PASSWORD"),
    }


def get_token() -> BearerToken:
    url = f"{base_url}/wp-json/jwt-auth/v1/token"
    response = requests.post(
        url,
        data=_get_credentials(),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        return f"Bearer {response.json()["token"]}"
    else: 
        raise NoLLQJWTTokenException(
            f"Failed to get LLQ JWT Token for {_get_credentials()["username"]}. \nStatus code : {response.status_code}"
        )