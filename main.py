import os
import logging

from slack_bolt import App
from src.slack.create_job import create_job_modal
from src.slack.modal.modal_config import ModalCallbackIds
from config import Config

app = App(
    token=Config.SLACK_BOT_TOKEN,
    signing_secret=Config.SLACK_SIGN_IN_SECRET,
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
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())


@app.view(ModalCallbackIds.JOB.value)
def handle_view_submission_events(ack, body):
    ack()
    # job = map_to_job(body)
    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    # print(job)
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3100)))
