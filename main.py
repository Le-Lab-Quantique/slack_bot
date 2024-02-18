import os
import logging

from slack_bolt import App

from src.slack.create_job import create_job_modal, map_to_job
from src.llq_website.job.post_job import post_job_in_wordpress

app = App(
    token="",
    signing_secret="",
)

logging.basicConfig(level=logging.DEBUG)


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.command("/hello-world")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@app.shortcut("create_job_in_wp")
def open_modal(ack, shortcut, client):
    ack()
    client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())


@app.view("modal-submit-job")
def handle_view_submission_events(ack, body):
    ack()
    post_job_in_wordpress(map_to_job(body))


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
