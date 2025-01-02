import json

from src.slack.job.job_definition import JobActionsId
from src.slack.modal.modal_config import (
    DropdownElement,
    InputConfig,
    Modal,
    ModalsCallbackId,
)

from ..utils import process_body_result
from dataclasses import dataclass
from llq.type.job import Job
from llq.type import Node, MediaItem
from typing import Optional 

company_config = InputConfig(
    "Structure",
    JobActionsId.COMPANY,
    "Select a structure",
    options=[
        DropdownElement(text=company["partners"]["partner_name"], value=company["id"])
        for company in [] # TODO: Replace with real list 
    ],
)
title_config = InputConfig("Job Title", JobActionsId.TITLE_ACTION, "Enter job title")
description_config = InputConfig(
    "Description",
    JobActionsId.DESCRIPTION,
    "Enter job description",
    is_multiline=True,
)
localization_config = InputConfig(
    "Localization", JobActionsId.LOCALIZATION, "Enter job localization"
)
contract_config = InputConfig(
    "Contract",
    JobActionsId.TYPE_OF_CONTRACT,
    "Select a contract",
    options=[
        DropdownElement(text=contract_type, value=None)
        for contract_type in [] # TODO : REPLACE 
    ],
)
post_config = InputConfig(
    "Sector",
    JobActionsId.TYPE_OF_POST,
    "Select a sector",
    options=[DropdownElement(text=job_type, value=None) for job_type in [] ], # TODO : REPLACE 
)
presence_config = InputConfig(
    "Presence",
    JobActionsId.PRESENCE,
    "Select a presence",
    options=[DropdownElement(text=presence, value=None) for presence in []], # TODO : REPLACE
)
apply_link_config = InputConfig(
    "Apply link", JobActionsId.APPLY_LINK, "Enter apply link", is_optional=True
)
contact_email_config = InputConfig(
    "Contact email",
    JobActionsId.CONTACT_EMAIL,
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
    presence_config,
    apply_link_config,
    contact_email_config,
]


def create_job_modal() -> str:
    modal = Modal(ModalsCallbackId.JOB, "Create a job offer.", configs)
    return json.dumps(modal, default=lambda o: o.__dict__)


@dataclass
class CreatedJobResult:
    job: Job
    partner: Optional[Node[MediaItem]]


def map_to_job(body: dict) -> CreatedJobResult:
    attributes = process_body_result(body)

    company_id = attributes.get("job_compagny_name_", None)
    if not company_id:
        raise ValueError("Company ID not found in attributes")

    partner = {} # TODO : REPLACE WITH REAL GET BY ID

    attributes["job_compagny_name_"] = partner.name
    attributes["job_compagny_logo"] = partner.database_id

    return CreatedJobResult(job=Job(**attributes), partner=partner)
