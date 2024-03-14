import logging
import os

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from config import load_config
from src.slack import register_listeners


env = os.environ.get("ENV")
config = load_config(env)

app: Flask = Flask(__name__, instance_relative_config=True)
slack_app = App(
    token=config.SLACK_BOT_TOKEN,
    signing_secret=config.SLACK_SIGN_IN_SECRET,
)


def create_app(environment=None) -> Flask:
    env = environment or os.environ.get("ENV")
    config = load_config(env)
    app.config.from_object(config)
    return app


def register_slack_handlers():
    logging.basicConfig(level=logging.DEBUG)
    register_listeners(slack_app)
    handler = SlackRequestHandler(slack_app)

    @app.route("/slack/events", methods=["POST"])
    def slack_events():
        return handler.handle(request)


register_slack_handlers()
