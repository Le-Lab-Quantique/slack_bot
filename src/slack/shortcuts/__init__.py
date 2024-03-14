from slack_bolt import App
from src.slack.shortcuts.job_shortcut import create_job_shortcut
from src.slack.shortcuts.shortcuts_id import ShortcutsId


def register(app: App):
    app.shortcut(ShortcutsId.JOB.value)(create_job_shortcut)
