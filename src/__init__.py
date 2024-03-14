import json
import logging
import os

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from config import Config, load_config
from src.slack import register_listeners

flask_app = Flask(__name__, instance_relative_config=True)


app = App(
    token=Config.SLACK_BOT_TOKEN,
    signing_secret=Config.SLACK_SIGN_IN_SECRET,
)

logging.basicConfig(level=logging.DEBUG)


register_listeners(app)


def create_app(environment=None) -> Flask:
    env = environment or os.environ.get("ENV")
    config = load_config(env)

    flask_app.config.from_object(config)

    return flask_app


handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
