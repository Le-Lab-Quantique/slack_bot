from src.llq_website.job.types import Job
from .utils import process_body_result
from src.llq_website.job.data import job_contract_types, job_types
from src.llq_website.partner.get_partners import get_partners
from src.slack.job.job_definition import JobActionIds, JobConfig
from src.slack.modal.modal_config import (
    build_dropdown_list_option,
    builld_modal_information,
    ModalCallbackIds,
)


company_config = JobConfig(
    "Structure",
    JobActionIds.COMPANY,
    "Select a structure",
    options=[
        build_dropdown_list_option(text=company["partners"]["partnerName"], value=None)
        for company in get_partners()
    ],
)
title_config = JobConfig("Job Title", JobActionIds.TITLE_ACTION, "Enter job title")
description_config = JobConfig(
    "Description",
    JobActionIds.DESCRIPTION,
    "Enter job description",
    is_multiline=True,
)
localization_config = JobConfig(
    "Localization", JobActionIds.LOCALIZATION, "Enter job localization"
)
contract_config = JobConfig(
    "Contract",
    JobActionIds.TYPE_OF_CONTRACT,
    "Select a contract",
    options=[
        build_dropdown_list_option(text=contract_type, value=None)
        for contract_type in job_contract_types
    ],
)
post_config = JobConfig(
    "Sector",
    JobActionIds.TYPE_OF_POST,
    "Select a sector",
    options=[
        build_dropdown_list_option(text=job_type, value=None) for job_type in job_types
    ],
)
apply_link_config = JobConfig(
    "Apply link", JobActionIds.APPLY_LINK, "Enter apply link", is_optional=True
)
contact_email_config = JobConfig(
    "Contact email",
    JobActionIds.CONTACT_EMAIL,
    "Enter contact email",
    is_optional=True,
)

configs = [
    company_config,
    title_config,
    description_config,
    localization_config,
    contract_config,
    post_config,
    apply_link_config,
    contact_email_config,
]


def generate_blocks(configs: list[JobConfig]) -> list[dict]:
    return [
        {
            "type": "input",
            "element": {
                "type": "static_select" if config.options else "plain_text_input",
                "placeholder": {
                    "type": "plain_text",
                    "text": config.placeholder,
                    "emoji": True,
                },
                **({"options": config.options} if config.options else {}),
                "action_id": config.action_id,
                **({"multiline": config.is_multiline} if config.is_multiline else {}),
            },
            "label": {"type": "plain_text", "text": config.label, "emoji": True},
            "optional": config.is_optional,
        }
        for config in configs
    ]


def create_job_modal() -> dict:
    return {
        **builld_modal_information(ModalCallbackIds.JOB.value, "Create a job offer."),
        "blocks": generate_blocks(configs),
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
