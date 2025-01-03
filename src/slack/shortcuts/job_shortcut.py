from src.slack.job.create_job import create_job_modal
from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

async def create_job_shortcut(ack: AsyncAck, shortcut, client: AsyncWebClient):
    await ack()
    await client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())
