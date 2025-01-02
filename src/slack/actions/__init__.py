from slack_bolt.async_app import AsyncApp 
from .job_action import approve_job_action, reject_job_action
from src.slack.actions.actions_id import ActionsId


async def register(app: AsyncApp):
    app.action(ActionsId.APPROVE_JOB.value)(approve_job_action)
    app.action(ActionsId.REJECT_JOB.value)(reject_job_action)
