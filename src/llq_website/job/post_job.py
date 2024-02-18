import requests

from src.llq_website.get_llq_jwt_token import get_token
from src.llq_website.utils import WordPressPostStatus, base_url

from .types import Job

headers = {"Content-Type": "application/json", "Authorization": get_token()}


def post_job_in_wordpress(job: Job) -> dict:
    url = f"{base_url}/wp-json/wp/v2/job"
    job_post = {
        "title": job.title,
        "status": WordPressPostStatus.DRAFT,
        "acf": job.__dict__(),
    }
    response = requests.post(url, headers=headers, json=job_post)
    return response.json()
