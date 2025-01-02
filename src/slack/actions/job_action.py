from llq import DeleteJobMutation, UpdateJobStatusMutation
from llq.schema import PostStatusEnum

async def approve_job_action(say, body):
    job_id = body["actions"][0]["value"]
    update_job_status = UpdateJobStatusMutation()
    mutation = update_job_status.get(id=job_id, status=PostStatusEnum.PUBLISH)
    await say("Job is approved !")


async def reject_job_action(say, body):
    job_id = body["actions"][0]["value"]
    delete_job = DeleteJobMutation()
    mutation = delete_job.get(id=job_id) 
    await say("Job is rejected !")
