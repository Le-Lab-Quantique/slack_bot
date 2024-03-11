from typing import Optional
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
        self.url: str = f"{base_url}/wp-json/wp/v2/{slug}"
        self.headers: dict[str, str] = headers
        self.timeout: int = timeout
        self.retries: int = retries

    def get(self) -> dict:
        return self.make_request(method="GET")

    def post(self, data: dict) -> dict:
        return self.make_request(data=data)

    def update(self, data: dict) -> dict:
        return self.make_request(data=data, method="PUT")

    def delete(self):
        return self.make_request(method="DELETE")
