from slack_sdk.models.blocks import (
    SectionBlock,
    ImageElement,
    DividerBlock,
    ButtonElement,
    ActionsBlock,
    PlainTextObject,
    MarkdownTextObject
)
from slack_sdk.models.blocks import Block
from src.slack.job.create_job import CreatedJobResult
from src.slack.messages.posted_job_template import posted_job_template
from src.slack.actions.actions_id import ActionsId
from typing import Sequence

def create_confirm_or_reject_message(
    posted_job: CreatedJobResult, job_id: str
) -> Sequence[Block]:
    markdown_text = posted_job_template(posted_job)
    markdown = MarkdownTextObject(text=markdown_text)

    section = SectionBlock(text=markdown)

    image_url = posted_job.partner.partner_acf.partner_logo.node.media_item_url
    alt_text = posted_job.partner.partner_acf.partner_logo.node.alt_text or "partner logo"
    image = ImageElement(image_url=image_url, alt_text=alt_text)

    divider = DividerBlock()

    approve_button = ButtonElement(
        action_id=ActionsId.APPROVE_JOB.value,
        text=PlainTextObject(text="APPROVE ✔️"),
        value=job_id,
    )
    reject_button = ButtonElement(
        action_id=ActionsId.REJECT_JOB.value,
        text=PlainTextObject(text="REJECT ❌"),
        value=job_id,
    )

    actions = ActionsBlock(elements=[approve_button, reject_button])

    return [
        section,
        image, 
        divider,
        actions,
    ]
