from slack_bolt import App
from src.slack.views.job_view import handle_job_submission
from src.slack.modal.modal_config import ModalsCallbackId


def register(app: App):
    app.view(ModalsCallbackId.JOB.value)(handle_job_submission)
