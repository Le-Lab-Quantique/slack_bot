from src.slack.views.job_view import handle_job_submission
from src.slack.modal.modal_config import ModalsCallbackId
from slack_bolt.async_app import AsyncApp 

async def register(app: AsyncApp):
    app.view(ModalsCallbackId.JOB.value)(handle_job_submission)
