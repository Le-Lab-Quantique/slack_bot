from dataclasses import asdict
from uuid_utils import uuid7

from src.llq_website.get_llq_jwt_token import get_token
from src.llq_website.utils import WordPressPostStatus
from src.llq_website.client.rest_client import RESTClient

from .types import Job

headers = {"Content-Type": "application/json", "Authorization": get_token()}


def post_job_in_wordpress(job: Job) -> dict:
    job_post = {
        "title": job.job_title_,
        "status": WordPressPostStatus.DRAFT,
        "slug": str(uuid7()),
        "acf": asdict(job),
    }
    return RESTClient("job", headers=headers).post(data=job_post)
