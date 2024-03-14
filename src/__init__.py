import json
import logging
import os

from slack_bolt import App

from config import Config, load_config
from src.llq_website.job.post_job import (
    post_job_in_wordpress,
    delete_job,
    edit_job_status,
)
from src.slack.create_job import create_job_modal, map_to_job
from src.slack.modal.modal_config import ModalCallbackIds
from flask import Flask
from src.slack.message.message_config import create_confirm_or_reject_message
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import request


slack_app = App(
    token=Config.SLACK_BOT_TOKEN,
    signing_secret=Config.SLACK_SIGN_IN_SECRET,
)
flask_app = Flask(__name__, instance_relative_config=True)

logging.basicConfig(level=logging.DEBUG)


@slack_app.middleware
def log_request(logger, body, next):
    prettified_body = json.dumps(body, indent=4)
    logger.debug(prettified_body)
    return next()


@slack_app.command("/hello-world")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@slack_app.shortcut("create_job_in_wp")
def open_modal(ack, shortcut, client):
    ack()
    client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())


@slack_app.view(ModalCallbackIds.JOB.value)
def handle_view_submission_events(logger, ack, body, say):
    pending_jobs_channel_id = "C06P1M5J0HG"
    ack()
    processed_body = map_to_job(body)
    posted_job = post_job_in_wordpress(processed_body.job)
    posted_job_id = posted_job.get("id", "")
    say(
        blocks=create_confirm_or_reject_message(processed_body, str(posted_job_id)),
        channel=pending_jobs_channel_id,
        text="CONFIRM_JOB_MESSAGE",
    )


@slack_app.action("approve_job")
def approve_job(ack, say, body):
    job_id = body["actions"][0]["value"]
    edit_job_status(job_id)
    say("Job is approved !")


@slack_app.action("not_approve_job")
def unapprove_job(ack, say, body):
    job_id = body["actions"][0]["value"]
    delete_job(job_id)
    say("Job is rejected !")


def create_app(environment=None) -> Flask:
    env = environment or os.environ.get("ENV")
    config = load_config(env)

    flask_app.config.from_object(config)

    return flask_app


handler = SlackRequestHandler(slack_app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
