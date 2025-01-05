from slack_sdk.models.blocks import (
    ActionsBlock,
    ContextBlock,
    DividerBlock,
    HeaderBlock,
    ImageElement,
    LinkButtonElement,
    PlainTextObject,
    SectionBlock,
    Block,
)
from llq.type.event import Event
from src.utils import format_date_string
from typing import Sequence


def no_upcoming_events() -> Sequence[Block]:
    """
    Returns a Slack message block for when no events are available.
    """
    return [
        SectionBlock(
            text=":warning: *No upcoming events found!* \n"
                 "Stay tuned for the latest updates on future events."
        )
    ]


def build_event_details_message(event: Event) -> Sequence[Block]:
    """
    Creates a detailed Slack message for the next event, including organizer,
    date, location, and a call-to-action button.
    """
    organizer = (
        event.organizers.nodes[0].title if event.organizers else "Le Lab Quantique"
    )
     
    if event.all_day:
        date_info = f"📅 Full Day: *{format_date_string(event.start_date)}*"
    else:
        date_info = (
            f"📅 From: *{format_date_string(event.start_date)}* \n"
            f"📅 To: *{format_date_string(event.end_date)}*"
        )
 
    city = event.venue.city if event.venue else "Unknown City"
    address = event.venue.address if event.venue else "Address not available"
 
    event_details = (
        f"🎉 *Organized by*: *{organizer}* \n"
        f"{date_info} \n"
        f"📍 {city}, {address} \n"
        f"\n Don't miss this incredible event!"
    )
 
    header = HeaderBlock(text=event.title)
    main_content = SectionBlock(
        text=event_details,
        accessory=ImageElement(
            alt_text="Event thumbnail or Le Lab Quantique logo",
            image_url=(
                event.featured_image.node.source_url
                if event.featured_image
                else "https://lelabquantique.com/wp-content/uploads/2024/01/cropped-picto.png"
            ),
        ),
    )
    details_button = ActionsBlock(
        elements=[
            LinkButtonElement(
                text=PlainTextObject(text="🔗 View Event Details"),
                url=event.link,
                style="primary",
            ),
        ],
    )
    divider = DividerBlock()
    metadata = ContextBlock(
        elements=[PlainTextObject(text=f"🕒 Event Created On: {format_date_string(event.date)}")]
    )

    return [header, main_content, details_button, divider, metadata]
