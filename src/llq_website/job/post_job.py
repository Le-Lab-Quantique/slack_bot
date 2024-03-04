import requests
from dataclasses import asdict
from uuid_utils import uuid7

from src.llq_website.get_llq_jwt_token import get_token
from src.llq_website.utils import WordPressPostStatus, base_url

from .types import Job

headers = {"Content-Type": "application/json", "Authorization": get_token()}


def post_job_in_wordpress(job: Job) -> dict:
    url = f"{base_url}/wp-json/wp/v2/job"
    job_post = {
        "title": job.job_title_,
        "status": WordPressPostStatus.DRAFT,
        "slug": str(uuid7()),
        "acf": asdict(job),
    }
    response = requests.post(url, headers=headers, json=job_post)
    return response.json()
