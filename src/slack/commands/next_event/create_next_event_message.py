from datetime import datetime

from slack_sdk.models.blocks import (
    ActionsBlock,
    ContextBlock,
    DividerBlock,
    HeaderBlock,
    ImageElement,
    LinkButtonElement,
    PlainTextObject,
    SectionBlock,
)

from src.llq_website.next_event.next_event_types import Event


def _format_date(date: str) -> str:
    try:
        formats_to_try = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
        for date_format in formats_to_try:
            try:
                parsed_date = datetime.strptime(date, date_format)
                return parsed_date.strftime("%A, %B %d, %Y at %I:%M %p")
            except ValueError:
                pass
        return "Invalid date format"
    except Exception as e:
        return f"Error: {e}"


def create_next_event_message(event: Event) -> list:
    organizer = (
        event.organizers.nodes[0].title
        if len(event.organizers.nodes) == 1
        else "Le Lab Quantique"
    )

    formatted_non_full_day_date = f"From : *{_format_date(event.start_date)}* \n To : *{_format_date(event.end_date)}*"
    formatted_full_day_date = f"Full day : *{_format_date(event.start_date)}*"
    select_good_date_format = (
        formatted_full_day_date if event.all_day else formatted_non_full_day_date
    )

    header = HeaderBlock(text=event.title)
    main_content = SectionBlock(
        text=f"Organized by : *{organizer}* \n {select_good_date_format} \n\n {event.venue.city}, {event.venue.address} ",
        accessory=ImageElement(
            alt_text="Image represent event or Le Lab Quantique",
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
        elements=[PlainTextObject(text=f"Created : {_format_date(event.date)}")]
    )

    return [header, main_content, details_button, divider, created_at]
