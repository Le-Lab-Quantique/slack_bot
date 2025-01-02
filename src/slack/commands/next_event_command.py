from slack_bolt.async_app import AsyncAck, AsyncRespond
from src.slack.commands.next_event.create_next_event_message import (
    create_next_event_message,
)
from llq import EventByStartDateQuery

async def handle_next_event_command(ack: AsyncAck, respond: AsyncRespond) -> None:
    event = EventByStartDateQuery()
    event_query = event.get(first=1, start_date=None)
    await ack()
    await respond(
        replace_original=False,
        blocks=create_next_event_message(event),
    )
