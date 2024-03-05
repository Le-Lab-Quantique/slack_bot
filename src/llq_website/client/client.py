from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from .exceptions import ClientException


class Client:
    ERROR_STATUS = [404, 500, 502, 503, 504]

    def __init__(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = 0,
    ) -> None:
        self.url: str = url
        self.headers: dict[str, str] = headers
        self.timeout: int = timeout
        self.retries: int = retries

    def get(self) -> dict:
        """Overrides Client.get()"""
        pass

    def post(self, data: dict) -> dict:
        """Overrides Client.post()"""
        pass

    def make_request(self, data: dict, method: str = "POST") -> dict:
        """
        Sends a POST request to the API endpoint with the specified json body.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ClientException: If the request to the API fails or returns a non-200 status code.
        """
        session = self._create_retry_session()
        for _ in range(self.retries + 1):
            response = (
                self._send_post_request(session, data)
                if method.upper() == "POST"
                else self._send_get_request(session)
            )
            if response.status_code not in self.ERROR_STATUS:
                return response.json()
            else:
                raise ClientException(
                    f"\n status: {response.status_code} \n message : client issue.  \n json: {data} "
                )
        raise ClientException(f"Failed to make request, after : {self.retries} retries")

    def _send_post_request(self, session: requests.Session, data: dict):
        response = session.post(
            self.url,
            json=data,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response

    def _send_get_request(self, session: requests.Session):
        response = session.get(
            self.url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response

    def _create_retry_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=1,
            status_forcelist=self.ERROR_STATUS,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session
