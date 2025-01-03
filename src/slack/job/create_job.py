from dataclasses import dataclass
from typing import Optional, List, Sequence, Callable, Any, Dict, TypeVar, Coroutine

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
from llq.queries.job import TermsResponse
from llq.queries.partner import PartnersResponse, PartnerType
from ..utils import process_body_result

CREATE_JOB_CALLBACK_ID = "create_job_modal"

# Type variables for input and output
TQuery = TypeVar("TQuery", bound=Callable[..., Any])
TResponse = TypeVar("TResponse")

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

def async_fetch_data(
    client: GraphQLClient,
    query_func: TQuery,
    parser: Callable[[dict], TResponse],
) -> Callable[..., Coroutine[Any, Any, TResponse]]:
    async def fetch(**query_args: Dict[str, Any]) -> TResponse:
        query_instance = query_func(**query_args) 
        response = await client.execute(query_instance) 
        return parser(response) 
    return fetch

fetch_custom_terms = async_fetch_data(GraphQLClient, CustomTermsQuery, TermsResponse.parse)
fetch_partners = async_fetch_data(GraphQLClient, PartnersQuery, PartnersResponse.parse)
fetch_partner_by_id = async_fetch_data(GraphQLClient, PartnerByIdQuery, PartnerByIdQuery.parse)

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

async def create_select_block_from_data(
    client: GraphQLClient,
    label: str,
    action_id: str,
    placeholder: str,
    term_type: Optional[str] = None,
) -> InputBlock:
    custom_terms = await fetch_custom_terms(client, first=100)
    data = getattr(custom_terms, term_type).nodes

    options = [
        Option(text=PlainTextObject(text=item.name), value=getattr(item, 'uri', item.id))
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
        await create_select_block_from_data(
            client,
            label="Contract",
            action_id=ActionId.CONTRACT_KIND,
            placeholder="Select a contract",
            term_type="contract_kinds",
        ),
        await create_select_block_from_data(
            client,
            label="Sector",
            action_id=ActionId.OCCUPATION_KIND,
            placeholder="Select a sector",
            term_type="occupation_kinds",
        ),
        await create_select_block_from_data(
            client,
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
    partner: PartnerType

async def map_to_job(client: GraphQLClient, body: dict) -> CreatedJobResult:
    attributes = process_body_result(body)

    company_id = attributes.get(ActionId.COMPANY, None)
    if not company_id:
        raise ValueError("Company ID not found in attributes")

    partner: PartnerType = await fetch_partner_by_id(client=client, id=company_id)

    attributes[ActionId.COMPANY] = partner.partner_acf.partner_name
    attributes["job_company_logo"] = partner.partner_acf.partner_logo.node.database_id

    return CreatedJobResult(job=CreateJobAcf(**attributes), partner=partner)
