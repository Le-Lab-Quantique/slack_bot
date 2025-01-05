import logging
import os
from typing import Optional 
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from aiohttp import web
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from config import load_config
from src.slack import register_listeners
from llq import GraphQLClient, RestClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_ENV = "development"
HEALTHCHECK_ROUTE = "/health"

env = os.environ.get("ENV", DEFAULT_ENV)
config = load_config(env)

app = AsyncApp(token=config.SLACK_BOT_TOKEN)
graphql_client = GraphQLClient(endpoint_url=config.GRAPHQL_ENDPOINT)
socket_mode_client: Optional[SocketModeClient] = None

class GraphQLMiddleware(AsyncMiddleware):
    def __init__(self, client: GraphQLClient):
        self.client = client

    async def async_process(self, *, req, resp, next):
        req.context["graphql_client"] = self.client
        return await next()

async def start_services(web_app: web.Application):
    """
    Start Socket Mode client and GraphQL client.
    """
    global socket_mode_client
    try:
        handler = AsyncSocketModeHandler(app, config.SLACK_APP_TOKEN)
        await handler.connect_async()
        socket_mode_client = handler.client
        logger.info("Socket Mode client connected successfully")
    
        await graphql_client.connect()
        logger.info("GraphQL client initialized")
        
        await register_listeners(app)
        logger.info("Listeners registered successfully")
        
    except Exception as e:
        logger.error(f"Failed to start services: {e}")
        raise


async def shutdown_services(web_app: web.Application):
    """
    Shutdown Socket Mode and GraphQL clients.
    """
    try:
        if socket_mode_client:
            await socket_mode_client.close()
            logger.info("Socket Mode client closed successfully")
        await graphql_client.close()
        logger.info("GraphQL client closed successfully")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


async def healthcheck_handler(_req: web.Request) -> web.Response:
    """
    Health check endpoint to verify Socket Mode client status.
    """
    if socket_mode_client and socket_mode_client.is_connected():
        return web.Response(status=200, text="OK")
    logger.warning("Socket Mode client is inactive")
    return web.Response(status=503, text="The Socket Mode client is inactive")


async def setup_web_app() -> web.Application:
    """
    Set up and configure the web application with services and healthcheck.
    """
    web_app = app.web_app(port=config.PORT)
    web_app.add_routes([web.get(HEALTHCHECK_ROUTE, healthcheck_handler)])
    web_app.on_startup.append(start_services)
    web_app.on_cleanup.append(shutdown_services)
    logger.info("Web application setup complete")
    return web_app

app.use(GraphQLMiddleware(graphql_client))