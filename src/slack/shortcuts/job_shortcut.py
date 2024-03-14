from src.slack.job.create_job import create_job_modal


def create_job_shortcut(ack, shortcut, client):
    ack()
    client.views_open(trigger_id=shortcut["trigger_id"], view=create_job_modal())
