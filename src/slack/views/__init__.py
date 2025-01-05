from src.slack.views.job_view import handle_job_submission
from slack_bolt.async_app import AsyncApp 
from src.slack.job.create_job import CREATE_JOB_CALLBACK_ID

async def register(app: AsyncApp):
    app.view(CREATE_JOB_CALLBACK_ID)(handle_job_submission)
