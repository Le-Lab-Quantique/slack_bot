import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    LLQ_USERNAME = os.environ.get("LLQ_USERNAME")
    LLQ_PASSWORD = os.environ.get("LLQ_PASSWORD")
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_SIGN_IN_SECRET = os.environ.get("SLACK_SIGN_IN_SECRET")
    PORT = os.environ.get("PORT", 3001)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    PORT = os.environ.get("PORT", 80)


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SLACK_BOT_TOKEN = ""
    SLACK_SIGN_IN_SECRET = ""


def load_config(env: str) -> Config:
    config_switch = {
        "production": ProductionConfig,
        "testing": TestingConfig,
        "development": DevelopmentConfig,
    }

    config = config_switch.get(env, DevelopmentConfig)
    config.ENV = env

    return config
