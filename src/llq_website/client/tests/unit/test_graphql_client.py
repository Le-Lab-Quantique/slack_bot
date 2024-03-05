from unittest.mock import MagicMock, patch

import pytest

from src.llq_website.client.graphql_client import GraphQLClient


@pytest.fixture
def mock_graphql_client_request():
    with patch("src.llq_website.client.client.Client._send_post_request") as mock_post:
        yield mock_post


def test_graphql_client_should_return_200_status(
    app_context, mock_graphql_client_request
):
    query = """
    query {
        generalSettings {
            title
            url
        }
    }
    """

    client = GraphQLClient(query=query)

    expected_response = {
        "data": {
            "generalSettings": {
                "title": "Le Lab Quantique",
                "url": "https://lelabquantique.com",
            }
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = expected_response
    mock_graphql_client_request.return_value = mock_response

    response = client.get()

    assert response == expected_response
