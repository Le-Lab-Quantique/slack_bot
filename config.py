import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    LLQ_USERNAME = os.environ.get("LLQ_USERNAME")
    LLQ_PASSWORD = os.environ.get("LLQ_PASSWORD")
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_SIGN_IN_SECRET = os.environ.get("SLACK_SIGN_IN_SECRET")
    PORT = os.environ.get("PORT", 3001)
