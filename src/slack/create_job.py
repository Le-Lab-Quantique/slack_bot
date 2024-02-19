from enum import Enum

from src.llq_website.job.types import Job
from .utils import process_body_result
from src.llq_website.job.data import job_contract_types, job_types
from src.llq_website.partner.get_partners import get_partners

from typing import Optional


class JobActionIds(Enum):
    TITLE_ACTION = "job_title-action"
    CONTACT_EMAIL = "job_contact_email-action"
    DESCRIPTION = "job_description-action"
    LOCALIZATION = "job_localization-action"
    TYPE_OF_CONTRACT = "job_type_of_contract-action"
    TYPE_OF_POST = "job_type_of_post-action"
    DESCRIPTION_FILE = "job_description_file-action"
    APPLY_LINK = "job_apply_link-action"
    COMPANY = "job_company-action"


def basic_modal_information(modal_id: str, title: str) -> dict:
    return {
        "type": "modal",
        "callback_id": modal_id,
        "title": {"type": "plain_text", "text": title},
        "close": {"type": "plain_text", "text": "Close"},
        "submit": {"type": "plain_text", "text": "Submit"},
    }


def build_dropdown_list_option(text: str, value: Optional[str]) -> dict:
    return {
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True,
        },
        "value": value if value else text,
    }


def build_type_of_contract_option() -> list[dict]:
    return [
        build_dropdown_list_option(text=contract_type, value=None)
        for contract_type in job_contract_types
    ]


def build_job_type_option() -> list[dict]:
    return [
        build_dropdown_list_option(text=job_type, value=None) for job_type in job_types
    ]


def build_company_option() -> list[dict]:
    return [
        build_dropdown_list_option(text=company["partners"]["partnerName"], value=None)
        for company in get_partners()
    ]


def create_job_modal() -> dict:
    return {
        **basic_modal_information("modal-submit-job", "Create a job offer."),
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an structure",
                        "emoji": False,
                    },
                    "options": build_company_option(),
                    "action_id": JobActionIds.COMPANY.value,
                },
                "label": {"type": "plain_text", "text": "Structure", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": JobActionIds.TITLE_ACTION.value,
                },
                "label": {"type": "plain_text", "text": "Job Title", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": JobActionIds.DESCRIPTION.value,
                },
                "label": {"type": "plain_text", "text": "Description", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": JobActionIds.LOCALIZATION.value,
                },
                "label": {"type": "plain_text", "text": "Localization", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": build_type_of_contract_option(),
                    "action_id": JobActionIds.TYPE_OF_CONTRACT.value,
                },
                "label": {"type": "plain_text", "text": "Contract", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": build_job_type_option(),
                    "action_id": JobActionIds.TYPE_OF_POST.value,
                },
                "label": {"type": "plain_text", "text": "Sector", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": JobActionIds.APPLY_LINK.value,
                },
                "optional": True,
                "label": {"type": "plain_text", "text": "Apply link", "emoji": True},
            },
            {
                "type": "input",
                "element": {
                    "type": "email_text_input",
                    "action_id": JobActionIds.CONTACT_EMAIL.value,
                },
                "optional": True,
                "label": {"type": "plain_text", "text": "Contact email", "emoji": True},
            },
        ],
    }


def map_to_job(body: dict) -> Job:
    attribute_map = {
        "job_title_": JobActionIds.TITLE_ACTION.value,
        "job_description_": JobActionIds.CONTACT_EMAIL.value,
    }
    attributes = {
        key: process_body_result(body).get(mapping, "")
        for key, mapping in attribute_map.items()
    }
    return Job(**attributes)
