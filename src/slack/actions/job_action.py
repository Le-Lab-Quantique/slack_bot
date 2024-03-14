from src.llq_website.job.post_job import (
    delete_job,
    edit_job_status,
)


def approve_job_action(say, body):
    job_id = body["actions"][0]["value"]
    edit_job_status(job_id)
    say("Job is approved !")


def reject_job_action(say, body):
    job_id = body["actions"][0]["value"]
    delete_job(job_id)
    say("Job is rejected !")
