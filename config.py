import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    LLQ_USERNAME = os.environ.get("LLQ_USERNAME")
    LLQ_PASSWORD = os.environ.get("LLQ_PASSWORD")
    LLQ_ENDPOINT = os.environ.get("LLQ_ENDPOINT")
    GRAPHQL_ENDPOINT = f"{LLQ_ENDPOINT}/graphql"
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_SIGN_IN_SECRET = os.environ.get("SLACK_SIGN_IN_SECRET")
    SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
    PORT = int(os.environ.get("PORT", 3001))

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SLACK_BOT_TOKEN = ""
    SLACK_SIGN_IN_SECRET = ""
    SLACK_APP_TOKEN = ""
    ENDPOINT = "https://lelabquantique.com"


def load_config(env: str) -> Config:
    config_switch = {
        "production": ProductionConfig,
        "testing": TestingConfig,
        "development": DevelopmentConfig,
    }

    config = config_switch.get(env, DevelopmentConfig)
    config.ENV = env

    return config
