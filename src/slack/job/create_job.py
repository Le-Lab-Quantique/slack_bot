from dataclasses import dataclass
from typing import Optional, List, Sequence, Any

from slack_sdk.models.views import View
from slack_sdk.models.blocks import (
    InputBlock,
    PlainTextObject,
    StaticSelectElement,
    Option,
    Block,
    PlainTextInputElement,
)
from llq.type.job import CreateJobAcf
from llq import GraphQLClient, CustomTermsQuery, PartnersQuery, PartnerByIdQuery
from llq.type.partner import Partner
from src.utils import async_fetch, process_body_result

CREATE_JOB_CALLBACK_ID = "create_job_modal"

class ActionId:
    TITLE = "job_title_"
    DESCRIPTION = "job_description_"
    LOCALIZATION = "job_localization_"
    APPLY_LINK = "job_apply_link"
    CONTACT_EMAIL = "job_contact_email"
    JOB_MODE = "job_presence_"
    CONTRACT_KIND = "job_type_of_contract_"
    OCCUPATION_KIND = "job_type_of_post_"
    COMPANY = "job_compagny_name_"

fetch_custom_terms = async_fetch(CustomTermsQuery, CustomTermsQuery.parse)
fetch_partners = async_fetch(PartnersQuery, PartnersQuery.parse)
fetch_partner_by_id = async_fetch(PartnerByIdQuery, PartnerByIdQuery.parse)

def create_static_select_block(
    label: str,
    action_id: str,
    placeholder: str,
    options: List[Option],
) -> InputBlock:
    select_element = StaticSelectElement(
        action_id=action_id,
        placeholder=PlainTextObject(text=placeholder),
        options=options,
        initial_option=options[0] if options else None,
    )
    return InputBlock(
        label=PlainTextObject(text=label),
        element=select_element,
    )

def create_select_block_from_fetched_data(
    custom_terms,
    label: str,
    action_id: str,
    placeholder: str,
    term_type: Optional[str] = None,
) -> InputBlock:
    data = getattr(custom_terms, term_type).nodes
    options = [
        Option(text=PlainTextObject(text=item.name), value=item.name)
        for item in data
    ]
    return create_static_select_block(label, action_id, placeholder, options)

async def create_select_compagnies_input(client: GraphQLClient) -> InputBlock:
    partners = await fetch_partners(client, first=60)
    options = [
        Option(text=PlainTextObject(text=partner.partner_acf.partner_name), value=partner.id)
        for partner in partners.partners.nodes
    ]
    return create_static_select_block(
        label="Select a company",
        action_id=ActionId.COMPANY,
        placeholder="Choose a company",
        options=options,
    )

def create_plain_text_input_block(
    label: str,
    action_id: str,
    placeholder: str,
    is_multiline: bool = False,
    is_optional: bool = False,
) -> InputBlock:
    text_input = PlainTextInputElement(
        action_id=action_id,
        placeholder=PlainTextObject(text=placeholder),
        multiline=is_multiline,
    )
    return InputBlock(
        label=PlainTextObject(text=label),
        element=text_input,
        optional=is_optional,
    )

async def create_job_modal(client: GraphQLClient) -> View:
    custom_terms = await fetch_custom_terms(client, first=100)
    input_blocks: Sequence[Block] = [
        create_plain_text_input_block(
            label="Job Title",
            action_id=ActionId.TITLE,
            placeholder="Enter job title",
        ),
        create_plain_text_input_block(
            label="Description",
            action_id=ActionId.DESCRIPTION,
            placeholder="Enter job description",
            is_multiline=True,
        ),
        create_plain_text_input_block(
            label="Localization",
            action_id=ActionId.LOCALIZATION,
            placeholder="Enter job localization",
        ),
        await create_select_compagnies_input(client),
        create_select_block_from_fetched_data(
            custom_terms=custom_terms,
            label="Contract",
            action_id=ActionId.CONTRACT_KIND,
            placeholder="Select a contract",
            term_type="contract_kinds",
        ),
        create_select_block_from_fetched_data(
            custom_terms=custom_terms,
            label="Sector",
            action_id=ActionId.OCCUPATION_KIND,
            placeholder="Select a sector",
            term_type="occupation_kinds",
        ),
        create_select_block_from_fetched_data(
            custom_terms=custom_terms,
            label="Presence",
            action_id=ActionId.JOB_MODE,
            placeholder="Select a job mode",
            term_type="job_modes",
        ),
        create_plain_text_input_block(
            label="Apply Link",
            action_id=ActionId.APPLY_LINK,
            placeholder="Enter apply link",
            is_optional=True,
        ),
        create_plain_text_input_block(
            label="Contact Email",
            action_id=ActionId.CONTACT_EMAIL,
            placeholder="Enter contact email",
            is_optional=True,
        ),
    ]

    return View(
        type="modal",
        callback_id=CREATE_JOB_CALLBACK_ID,
        title=PlainTextObject(text="Create a Job Offer"),
        blocks=input_blocks,
        submit=PlainTextObject(text="Submit"),
        close=PlainTextObject(text="Cancel"),
    )

@dataclass
class CreatedJobResult:
    job: CreateJobAcf
    partner: Partner
    contract_kinds: list[str]
    occupation_kinds: list[str]
    job_modes: list[str]

async def init_job_input(client: GraphQLClient, body: dict[str, Any]) -> CreatedJobResult:
    attributes = process_body_result(body)
    contract_kinds = attributes.pop("job_type_of_contract_")
    job_modes = attributes.pop("job_presence_")
    occupation_kinds = attributes.pop("job_type_of_post_")

    company_id = attributes.get(ActionId.COMPANY, None)
    if not company_id:
        raise ValueError("Company ID not found in attributes")

    result = await fetch_partner_by_id(client=client, id=company_id)
    partner = result.partner.partner_acf

    attributes[ActionId.COMPANY] = partner.partner_name
    attributes["job_compagny_logo"] = partner.partner_logo.node.database_id

    return CreatedJobResult(job=CreateJobAcf(**attributes), partner=partner, occupation_kinds=occupation_kinds, job_modes=job_modes, contract_kinds=contract_kinds)
