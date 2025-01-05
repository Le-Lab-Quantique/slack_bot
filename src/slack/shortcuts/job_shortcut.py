from src.slack.job.create_job import create_job_modal
from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.context import BoltContext
from llq import GraphQLClient

async def create_job_shortcut(ack: AsyncAck, shortcut, client: AsyncWebClient, context: BoltContext):
    await ack()
    graphql_client: GraphQLClient = context["graphql_client"]
    view = await create_job_modal(client=graphql_client) 
    await client.views_open(trigger_id=shortcut["trigger_id"], view=view)
