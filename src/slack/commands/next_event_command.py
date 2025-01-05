from slack_bolt.async_app import AsyncAck, AsyncRespond
from src.slack.commands.next_event.create_next_event_message import (
    no_upcoming_events, build_event_details_message
)
from llq import EventByStartDateQuery, GraphQLClient
from src.utils import async_fetch
from slack_bolt.context.context import BoltContext
from datetime import datetime

fetch_next_event = async_fetch(EventByStartDateQuery, EventByStartDateQuery.parse)

async def handle_next_event_command(ack: AsyncAck, respond: AsyncRespond, context: BoltContext) -> None:
    await ack() 
    current_date = datetime.now()  
    graphql_client: GraphQLClient = context["graphql_client"] 
    result = await fetch_next_event(client=graphql_client, first=1, date={
        "year": current_date.year,
        "month": current_date.month,
        "day": current_date.day,
    })
    events = result.events.nodes
    if len(events) != 0:
        await respond(
            replace_original=False,
            blocks=build_event_details_message(events[0]),
        )
    else:  
        await respond(
                replace_original=False,
                blocks=no_upcoming_events()
        )
   
