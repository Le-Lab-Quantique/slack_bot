from src.slack.channels_id import ChannelIds
from src.slack.job.create_job import init_job_input, CreatedJobResult
from src.slack.job.create_job_message import create_confirm_or_reject_message
from slack_bolt.async_app import AsyncAck, AsyncSay
from llq import post_job, GraphQLClient, RestClient, UpdateJobMutation
from llq.schema import PostStatusEnum
from llq.type.job import Job
from typing import Any
from src.auth import get_jwt_token
from config import Config

async def _create_job(
    gql_client: GraphQLClient, rest_client: RestClient, input: CreatedJobResult
) -> tuple[int, Job | None]:
    posted_job_acf = await post_job(input.job, rest_client)
    job_id = posted_job_acf.get("id", None)
    if not job_id:
        raise ValueError("Job ID not found in attributes")
    occupation_kind_input = {
        "append": True,
        "nodes": [{"name": occupation} for occupation in input.occupation_kinds],
    }
    contract_kind_input = {
        "append": True,
        "nodes": [{"name": contract} for contract in input.contract_kinds],
    }
    job_mode_input = {
        "append": True,
        "nodes": [{"name": mode} for mode in input.job_modes],
    }
    update_job = UpdateJobMutation()
    response = await gql_client.execute(
        update_job.get(
            job_id=job_id,
            status=PostStatusEnum.DRAFT,
            contract_kinds=contract_kind_input,
            occupation_kinds=occupation_kind_input,
            job_modes=job_mode_input,
        )
    )
    return (job_id, update_job.parse(response).job)


async def handle_job_submission(
    ack: AsyncAck, body: dict[str, Any], say: AsyncSay
):
    await ack()
    token = await get_jwt_token()
    headers = {
        "Authorization": token
    }
    graphql_client = GraphQLClient(endpoint_url=Config.GRAPHQL_ENDPOINT, headers=headers) 
    await graphql_client.connect()
    rest_client = RestClient(base_url=Config.REST_ENDPOINT, headers=headers) 
    await rest_client.connect()
    prepared_job_input = await init_job_input(client=graphql_client, body=body)
    job_id, _ = await _create_job(
        gql_client=graphql_client, rest_client=rest_client, input=prepared_job_input
    )
    await say(
        blocks=create_confirm_or_reject_message(prepared_job_input, job_id),
        channel=ChannelIds.JOB_PENDING_REVIEW.value,
        text="CONFIRM_JOB_MESSAGE",
    )
    await graphql_client.close()
    await rest_client.close()
