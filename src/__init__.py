import json
import logging
import os

from slack_bolt import App

from config import Config, load_config
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


def build_job_preview(
    value, title: str, desc: str, img: str, alt_text: str
) -> list[dict]:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{title}*\n {desc}",
            },
        },
        {
            "type": "image",
            "title": {"type": "plain_text", "text": title, "emoji": True},
            "image_url": img,
            "alt_text": alt_text,
        },
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "action_id": "approve_job",
                    "text": {"type": "plain_text", "text": "APPROVE", "emoji": True},
                    "value": "ll",
                },
                {
                    "type": "button",
                    "action_id": "not_approve_job",
                    "text": {
                        "type": "plain_text",
                        "text": "NOT APPROVE",
                        "emoji": True,
                    },
                    "value": "jj",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Ler Ros", "emoji": True},
                    "value": "click_me_123",
                    "url": "https://google.com",
                },
            ],
        },
    ]


@app.view(ModalCallbackIds.JOB.value)
def handle_view_submission_events(logger, ack, body, say):
    pending_jobs_channel_id = "C06JZ4P0U2K"
    ack()
    processed_body = map_to_job(body)
    posted_job = post_job_in_wordpress(processed_body.job)
    posted_job_id = posted_job.get("id", "")
    say(
        blocks=build_job_preview(
            posted_job_id,
            processed_body.job.job_title_,
            processed_body.job.job_description_,
            processed_body.partner.media_item_url,
            processed_body.partner.alt_text,
        ),
        channel=pending_jobs_channel_id,
    )


@app.action("approve_job")
def approve_job(ack, say):
    say("Request approved 👍")


@app.action("not_approve_job")
def unapprove_job(ack, say):
    say("Request  NOT app,roved 👍")


def create_app(environment=None) -> Flask:
    env = environment or os.environ.get("ENV")
    config = load_config(env)
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)

    return app
