from llq import DeleteJobMutation, UpdateJobStatusMutation, GraphQLClient
from llq.schema import PostStatusEnum
from config import Config
from src.auth import get_jwt_token
from slack_bolt.async_app import AsyncSay, AsyncAck
from typing import Any


async def _authenticated_client() -> GraphQLClient:
    token = await get_jwt_token()
    headers = {"Authorization": token}
    client = GraphQLClient(endpoint_url=Config.GRAPHQL_ENDPOINT, headers=headers)
    await client.connect()
    return client


def _get_job_id_from_body(body: dict[str, Any]) -> str:
    try:
        job_id = body["actions"][0]["value"]
    except (KeyError, IndexError):
        raise ValueError("Missing job_id in Slack payload. 'actions' or 'value' is not present.")
    
    if not job_id:
        raise ValueError("job_id is empty in Slack payload.")
    
    return job_id


async def approve_job_action(ack: AsyncAck, say: AsyncSay, body: dict[str, Any]):
    await ack()
    job_id = _get_job_id_from_body(body)
    client = await _authenticated_client()
    try:
        mutation = UpdateJobStatusMutation()
        response = await client.execute(mutation.get(id=job_id, status=PostStatusEnum.PUBLISH))
        job = mutation.parse(response)
        if job:
            await say("Job is approved!")
        else:
            await say("Oops! Something went wrong. Please contact the admin.")
    finally:
        await client.close()


async def reject_job_action(ack: AsyncAck, say: AsyncSay, body: dict[str, Any]):
    await ack()
    job_id = _get_job_id_from_body(body)
    client = await _authenticated_client()
    try:
        mutation = DeleteJobMutation().get(id=job_id)
        response = await client.execute(mutation)
        job = DeleteJobMutation().parse(response)
        if job:
            await say("Job is rejected!")
        else:
            await say("Oops! Something went wrong. Please contact the admin.")
    finally: 
        await client.close()
