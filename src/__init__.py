import json
import logging
import os

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from config import load_config
from src.slack import register_listeners


def create_slack_app(environment=None) -> App:
    env = environment or os.environ.get("ENV")
    config = load_config(env)
    return App(
        token=config.SLACK_BOT_TOKEN,
        signing_secret=config.SLACK_SIGN_IN_SECRET,
    )


def create_app(environment=None) -> Flask:
    flask_app = Flask(__name__, instance_relative_config=True)
    env = environment or os.environ.get("ENV")
    config = load_config(env)
    flask_app.config.from_object(config)
    return flask_app


def register_slack_handlers(slack_app: App, flask_app: Flask):
    logging.basicConfig(level=logging.DEBUG)
    register_listeners(slack_app)
    handler = SlackRequestHandler(slack_app)

    @flask_app.route("/slack/events", methods=["POST"])
    def slack_events():
        return handler.handle(request)
