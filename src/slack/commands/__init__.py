from .hello_word_command import hello_world_command
from .next_event_command import handle_next_event_command
from .commands_id import CommandsId
from slack_bolt.async_app import AsyncApp 

async def register(app: AsyncApp):
    app.command(CommandsId.HELLO.value)(hello_world_command)
    app.command(CommandsId.NEXT_EVENT.value)(handle_next_event_command)
