from dataclasses import dataclass, asdict
from typing import Optional
from src.slack.create_job import CreatedJobResult
from src.slack.message.posted_job_template import posted_job_template


@dataclass
class PlainText:
    text: str
    emoji: bool = True
    type: str = "plain_text"


@dataclass
class Button:
    action_id: str
    text: PlainText
    value: str
    type: str = "button"


@dataclass
class Image:
    title: PlainText
    image_url: str
    alt_text: Optional[str] = None
    type: str = "image"


@dataclass
class Markdown:
    text: str
    type: str = "mrkdwn"


@dataclass
class Section:
    text: Markdown
    type: str = "section"


@dataclass
class Divider:
    type: str = "divider"


@dataclass
class Actions:
    elements: list[Button]
    type: str = "actions"


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
        action_id="approve_job", text=PlainText(text="APPROVE ✅"), value=job_id
    )
    reject_button = Button(
        action_id="not_approve_job", text=PlainText("REJECT ❎"), value=job_id
    )

    actions = Actions(elements=[approve_button, reject_button])

    return [asdict(section), asdict(image), asdict(divider), asdict(actions)]
