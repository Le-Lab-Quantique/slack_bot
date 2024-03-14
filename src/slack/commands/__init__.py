from slack_bolt import App
from .hello_word_command import hello_world_command
from .commands_id import CommandsId


def register(app: App):
    app.command(CommandsId.HELLO.value)(hello_world_command)
