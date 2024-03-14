from src.slack.job.create_job import CreatedJobResult


def posted_job_template(posted_job: CreatedJobResult) -> str:
    return f"*{posted_job.job.job_title_}*\n {posted_job.job.job_description_}"
