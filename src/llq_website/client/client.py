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

    def make_request(self, method: str = "POST", data: dict = None) -> dict:
        """
        Sends a POST request to the API endpoint with the specified json body.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ClientException: If the request to the API fails or returns a non-200 status code.
        """
        session = self._create_retry_session()
        for _ in range(self.retries + 1):
            response = self._send_request(session=session, method=method, data=data)
            if response.status_code not in self.ERROR_STATUS:
                return response.json()
            else:
                raise ClientException(
                    f"\n status: {response.status_code} \n message : client issue.  \n json: {data} "
                )
        raise ClientException(f"Failed to make request, after : {self.retries} retries")

    def _send_request(self, session: requests.Session, method: str, data: dict = None):
        """
        Sends a request to the API endpoint with the specified HTTP method and JSON body.

        Parameters:
            session (requests.Session): The requests Session object.
            method (str): The HTTP method to use (POST, GET, PUT, DELETE).
            data (dict, optional): The JSON body to send with the request (default is None).

        Returns:
            requests.Response: The response from the API.

        Raises:
            requests.HTTPError: If the request to the API fails or returns a non-200 status code.
        """
        request_method = {
            "POST": session.post,
            "GET": session.get,
            "PUT": session.put,
            "DELETE": session.delete,
        }.get(method.upper())

        if request_method is None:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response = request_method(
            self.url, json=data, headers=self.headers, timeout=self.timeout
        )

        response.raise_for_status()

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
