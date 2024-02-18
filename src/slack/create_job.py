from enum import Enum

from src.llq_website.job.types import Job
from .utils import process_body_result


class JobActionIds(Enum):
    TITLE_ACTION = "job_title-action"
    CONTACT_EMAIL = "job_contact_email-action"
    DESCRIPTION = "job_description-action"
    LOCALIZATION = "job_localization-action"
    TYPE_OF_CONTRACT = "job_type_of_contract-action"
    TYPE_OF_POST = "job_type_of_post-action"
    DESCRIPTION_FILE = "job_description_file-action"
    APPLY_LINK = "job_apply_link-action"


def basic_modal_information(modal_id: str, title: str) -> dict:
    return {
        "type": "modal",
        "callback_id": modal_id,
        "title": {"type": "plain_text", "text": title},
        "close": {"type": "plain_text", "text": "Close"},
        "submit": {"type": "plain_text", "text": "Submit"},
    }


def create_job_modal() -> dict:
    return {
        **basic_modal_information("modal-submit-job", "Create a job offer."),
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": JobActionIds.TITLE_ACTION.value,
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "email_text_input",
                    "action_id": JobActionIds.CONTACT_EMAIL.value,
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            },
        ],
    }


def map_to_job(body: dict) -> Job:
    attribute_map = {
        "title": "job_title-action",
        "contact_email": "job_contact_email-action",
    }
    attributes = {
        key: process_body_result(body).get(mapping, "")
        for key, mapping in attribute_map.items()
    }
    return Job(**attributes)
