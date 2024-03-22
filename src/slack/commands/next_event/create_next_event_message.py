from slack_sdk.models.blocks import (
    ActionsBlock,
    ContextBlock,
    DividerBlock,
    HeaderBlock,
    ImageElement,
    PlainTextObject,
    SectionBlock,
    LinkButtonElement,
    ButtonStyles,
)
from src.llq_website.next_event.next_event_types import Event


def create_next_event_message(event: Event) -> list:
    header = HeaderBlock(text=event.title)
    main_content = SectionBlock(
        text=f"Organized by : *{ str(event.organizers['nodes']['title']) }* *{event.start_date}* \n {event.end_date} \n ",
        accessory=ImageElement(
            alt_text="ALT",
            image_url=(
                event.featured_image.source_url
                if event.featured_image
                else "https://lelabquantique.com/wp-content/uploads/2024/01/cropped-picto.png"
            ),
        ),
    )
    details_button = ActionsBlock(
        elements=[
            LinkButtonElement(
                text=PlainTextObject(text="See details"),
                url=event.link,
                style="primary",
            ),
        ],
    )
    divider = DividerBlock()
    created_at = ContextBlock(
        elements=[PlainTextObject(text=f"Created at : {event.date}")]
    )

    return [header, main_content, details_button, divider, created_at]
