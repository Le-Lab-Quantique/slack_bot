from slack_bolt import App
from src.slack.shortcuts.job_shortcut import create_job_shortcut
from src.slack.shortcuts.shortcuts_id import ShortcutsId
from slack_bolt.async_app import AsyncApp 

async def register(app: AsyncApp):
    app.shortcut(ShortcutsId.JOB.value)(create_job_shortcut)
