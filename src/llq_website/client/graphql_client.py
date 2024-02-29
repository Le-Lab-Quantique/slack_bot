from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from .exceptions import GraphQLClientException

from src.llq_website.utils import base_url


class GraphQLClient:
    """
    A simple GraphQL client for making requests to a GraphQL API.

    Args:
        variables (dict[str, Any]): A dictionary containing the variables to be used in the GraphQL query.
        query (str): The GraphQL query string.
        headers (dict[str, str], optional): Custom HTTP headers to be included in the request. Default is None.
        timeout (int, optional): Timeout setting for the request in seconds. Default is None.
        retries (int, optional): Number of retries for failed requests. Default is 0.

    Attributes:
        url (str): The URL of the GraphQL API endpoint.
        variables (dict[str, Any]): A dictionary containing the variables to be used in the GraphQL query.
        query (str): The GraphQL query string.
        headers (dict[str, str]): Custom HTTP headers to be included in the request.
        timeout (int): Timeout setting for the request in seconds.
        retries (int): Number of retries for failed requests.

    Methods:
        get(): Sends a POST request to the GraphQL API endpoint with the specified query and variables.

    Raises:
        GraphQLClientException: If the request to the GraphQL API fails or returns a non-200 status code.

    Examples:
        >>> variables = {"id": 1}
        >>> query = "{ user(id: $id) { name } }"
        >>> headers = {"Authorization": "Bearer token"}
        >>> client = GraphQLClient(variables, query, headers=headers, timeout=10, retries=3)
        >>> response = client.get()
        >>> print(response)
        {'data': {'user': {'name': 'John Doe'}}}
    """

    ERROR_STATUS = [404, 500, 502, 503, 504]

    def __init__(
        self,
        variables: dict[str, Any],
        query: str,
        headers: dict[str, str] = None,
        timeout: int = None,
        retries: int = 0,
    ) -> None:
        self.url: str = f"{base_url}/graphql"
        self.variables: dict[str, Any] = variables
        self.query: str = query
        self.headers: dict[str, str] = headers
        self.timeout: int = timeout
        self.retries: int = retries

    def get(self) -> dict:
        """
        Sends a POST request to the GraphQL API endpoint with the specified query and variables.

        Returns:
            dict: The JSON response from the GraphQL API.

        Raises:
            GraphQLClientException: If the request to the GraphQL API fails or returns a non-200 status code.
        """
        session = self._create_retry_session()
        for _ in range(self.retries + 1):
            response = self._send_request(session)
            if response.status_code == 200:
                return response.json()
            elif response.status_code not in self.ERROR_STATUS:
                raise GraphQLClientException(
                    f"\n status: {response.status_code} \n message : GraphQL API issue.  \n variables : {self.variables} \n query : {self.query} "
                )
        raise GraphQLClientException(
            f"Failed to make request, after : {self.retries} retries"
        )

    def _send_request(self, session: requests.Session):
        response = session.post(
            self.url,
            json={"query": self.query, "varaibles": self.variables},
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
