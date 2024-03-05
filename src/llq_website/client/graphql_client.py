from typing import Any, Optional
from .client import Client

from src.llq_website.utils import base_url


class GraphQLClient(Client):
    """
    A simple GraphQL client for making requests to a GraphQL API.

    Args:
        query (str): The GraphQL query string.
        variables (dict[str, Any], optional): A dictionary containing the variables to be used in the GraphQL query.
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

    def __init__(
        self,
        query: str,
        variables: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = 0,
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
        json = {"query": self.query, "variables": self.variables}
        return self.make_request(data=json)
