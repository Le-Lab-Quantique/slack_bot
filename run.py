import os

from src import create_app, app
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import request

flask_app = create_app()

if __name__ == "__main__":
    handler = SlackRequestHandler(app)

    @flask_app.route("/slack/events", methods=["POST"])
    def slack_events():
        return handler.handle(request)

    flask_app.run(port=int(os.environ.get("PORT", 3100)), debug=True)
