from typing import Callable, Any, Dict, TypeVar, Coroutine
from llq import GraphQLClient

TQuery = TypeVar("TQuery", bound=Callable[..., Any])
TResponse = TypeVar("TResponse")

def async_fetch(
    query_func: TQuery,
    parser: Callable[[dict], TResponse],
) -> Callable[..., Coroutine[Any, Any, TResponse]]:
    async def fetch(client: GraphQLClient, **query_args: Dict[str, Any]) -> TResponse: 
        query_instance = query_func().get(**query_args) 
        response = await client.execute(query_instance) 
        return parser(response)
    return fetch