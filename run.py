import os

from src import create_app, create_slack_app, register_slack_handlers

slack_app = create_slack_app()
app = create_app()

if __name__ == "__main__":
    register_slack_handlers(flask_app=app, slack_app=slack_app)
    app.run(port=int(os.environ.get("PORT", 3100)), debug=True)
