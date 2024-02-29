import json
import logging
import os

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from config import Config
from src.llq_website.job.post_job import post_job_in_wordpress
from src.slack.create_job import create_job_modal, map_to_job
from src.slack.modal.modal_config import ModalCallbackIds
from flask import Flask, request


app = App(
    token=Config.SLACK_BOT_TOKEN,
    signing_secret=Config.SLACK_SIGN_IN_SECRET,
)
logging.basicConfig(level=logging.DEBUG)


@app.middleware
def log_request(logger, body, next):
    prettified_body = json.dumps(body, indent=4)
    logger.debug(prettified_body)
    return next()


@app.command("/hello-world")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@app.shortcut("create_job_in_wp")
def open_modal(ack, shortcut, client):
    ack()
    client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())


@app.view(ModalCallbackIds.JOB.value)
def handle_view_submission_events(ack, body):
    ack()
    job = map_to_job(body)
    post_job_in_wordpress(job)


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if __name__ == "__main__":
    flask_app.run(port=int(os.environ.get("PORT", 3100)), debug=True)
