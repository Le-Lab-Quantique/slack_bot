import logging
import os

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from config import load_config
from src.slack import register_listeners


env = os.environ.get("ENV")

app: Flask = Flask(__name__, instance_relative_config=True)


def create_slack_app(environment=None):
    config = load_config(environment or env)
    return App(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGN_IN_SECRET)


def create_app(environment=None) -> Flask:
    config = load_config(environment or env)
    app.config.from_object(config)
    return app


def register_slack_handlers():
    logging.basicConfig(level=logging.DEBUG)
    slack_app = create_slack_app()
    register_listeners(slack_app)
    handler = SlackRequestHandler(slack_app)

    @app.route("/slack/events", methods=["POST"])
    def slack_events():
        return handler.handle(request)


register_slack_handlers()
