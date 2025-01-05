from typing import Literal
from llq import GraphQLClient, LoginMutation
from .exceptions import NoLLQJWTTokenException
from config import Config

BearerToken = Literal["Bearer"]

def _get_credentials() -> dict[str, str]:
    return {
        "username": Config.LLQ_USERNAME,
        "password": Config.LLQ_PASSWORD,
    }

async def get_jwt_token() -> BearerToken:
    client = GraphQLClient(endpoint_url=Config.GRAPHQL_ENDPOINT)
    try:
        await client.connect()
        login_mutation = LoginMutation().get(input=_get_credentials()) 
        response = await client.execute(login_mutation) 
        credentials = LoginMutation().parse(response)
        if credentials.auth_token:
            return f"Bearer {credentials.auth_token}"
        else:
            raise NoLLQJWTTokenException(f"Failed to get LLQ JWT Token {login_mutation}")
    finally:
        await client.close()
