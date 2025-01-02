from src.slack.channels_id import ChannelIds
from src.slack.job.create_job import map_to_job
from src.slack.job.create_job_message import create_confirm_or_reject_message
from slack_bolt.async_app import AsyncAck, AsyncSay
from llq import post_job


async def handle_job_submission(ack: AsyncAck, body: dict, say: AsyncSay):
    await ack()
    processed_body = map_to_job(body)
    posted_job = post_job(processed_body.job)
    posted_job_id = posted_job.get("id", "")
    await say(
        blocks=create_confirm_or_reject_message(processed_body, str(posted_job_id)),
        channel=ChannelIds.JOB_PENDING_REVIEW.value,
        text="CONFIRM_JOB_MESSAGE",
    )
