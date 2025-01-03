from src.slack import actions
from src.slack import commands
from src.slack import shortcuts
from src.slack import views
from slack_bolt.async_app import AsyncApp 

async def register_listeners(app: AsyncApp):
    await actions.register(app)
    await commands.register(app)
    await shortcuts.register(app)
    await views.register(app)
