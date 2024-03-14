from dataclasses import asdict
from src.slack.job.create_job import CreatedJobResult
from src.slack.messages.message_config import (
    PlainText,
    Markdown,
    Section,
    Image,
    Divider,
    Button,
    Actions,
)
from src.slack.messages.posted_job_template import posted_job_template
from src.slack.actions.actions_id import ActionsId


def create_confirm_or_reject_message(
    posted_job: CreatedJobResult, job_id: str
) -> list[dict]:
    title = PlainText(text=posted_job.job.job_title_)
    markdown = Markdown(text=posted_job_template(posted_job))
    section = Section(text=markdown)

    image = Image(
        title=title,
        image_url=posted_job.partner.media_item_url,
        alt_text=posted_job.partner.alt_text or "partner logo",
    )

    divider = Divider()

    approve_button = Button(
        action_id=ActionsId.APPROVE_JOB.value,
        text=PlainText(text="APPROVE ✅"),
        value=job_id,
    )
    reject_button = Button(
        action_id=ActionsId.REJECT_JOB.value, text=PlainText("REJECT ❎"), value=job_id
    )

    actions = Actions(elements=[approve_button, reject_button])

    return [asdict(section), asdict(image), asdict(divider), asdict(actions)]
