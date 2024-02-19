import os
import logging

from slack_bolt import App
from src.llq_website.partner.get_partners import get_partners
from src.slack.create_job import create_job_modal

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
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    result = get_partners()
    print(result)
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())


@app.view("modal-submit-job")
def handle_view_submission_events(ack, body):
    ack()
    # job = map_to_job(body)
    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    # print(job)
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3100)))
