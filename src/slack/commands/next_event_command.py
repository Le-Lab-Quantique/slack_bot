from slack_bolt import Ack, Respond
from src.slack.commands.next_event.create_next_event_message import (
    create_next_event_message,
)
from src.llq_website.next_event.get_next_event import get_next_event


def handle_next_event_command(ack: Ack, respond: Respond) -> None:
    event = get_next_event()
    ack()
    respond(
        replace_original=False,
        blocks=create_next_event_message(event),
    )
