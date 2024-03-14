from src.llq_website.job.post_job import (
    post_job,
)

from src.slack.channels_id import ChannelIds
from src.slack.job.create_job import map_to_job
from src.slack.job.create_job_message import create_confirm_or_reject_message


def handle_job_submission(ack, body, say):
    ack()
    processed_body = map_to_job(body)
    posted_job = post_job(processed_body.job)
    posted_job_id = posted_job.get("id", "")
    say(
        blocks=create_confirm_or_reject_message(processed_body, str(posted_job_id)),
        channel=ChannelIds.JOB_PENDING_REVIEW.value,
        text="CONFIRM_JOB_MESSAGE",
    )
