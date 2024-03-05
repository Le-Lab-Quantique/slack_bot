from typing import Any, Optional
from .client import Client

from src.llq_website.utils import base_url


class RESTClient(Client):
    def __init__(
        self,
        slug: str,
        headers: Optional[dict[str, str]] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = 0,
    ) -> None:
        self.slug: str = slug
        self.headers: dict[str, str] = headers
        self.timeout: int = timeout
        self.retries: int = retries

    def get(self) -> dict:
        self.url = f"{base_url}/wp-json/wp/v2/{self.slug}"
        return self.make_request(method="GET")

    def post(self, data: dict) -> dict:
        self.url = f"{base_url}/wp-json/wp/v2/{self.slug}"
        return self.make_request(data=data)
