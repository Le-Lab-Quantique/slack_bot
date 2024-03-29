from dataclasses import asdict
from uuid_utils import uuid7

from src.llq_website.get_llq_jwt_token import get_token
from src.llq_website.utils import WordPressPostStatus
from src.llq_website.client.rest_client import RESTClient

from .types import Job


def get_headers() -> dict:
    return {"Content-Type": "application/json", "Authorization": get_token()}


def post_job(job: Job) -> dict:
    job_post = {
        "title": job.job_title_,
        "status": WordPressPostStatus.DRAFT,
        "slug": str(uuid7()),
        "acf": asdict(job),
    }
    return RESTClient("job", headers=get_headers()).post(data=job_post)


def edit_job_status(job_id: str):
    params = {
        "status": WordPressPostStatus.PUBLISHED,
    }
    return RESTClient(f"job/{job_id}", headers=get_headers()).update(data=params)


def delete_job(job_id: str):
    return RESTClient(f"job/{job_id}", headers=get_headers()).delete()
