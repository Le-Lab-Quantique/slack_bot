from datetime import datetime

from src.llq_website.client.graphql_client import GraphQLClient

from .next_event_types import Event, OrganizerData, Organizer, Venue

query = """
query getNextEvent($first: Int, $startDate: DateQueryInput) {
  events(first: $first, where: { startDateQuery: $startDate, orderby: {field: DATE, order: ASC} }) {
    nodes {
      title
      duration
      startDate
      endDate
      date
      allDay
      url
      link
      organizers {
        nodes {
          title
        }
      }
      eventsCategories {
        nodes {
          name
        }
      }
      featuredImage {
        node {
          sourceUrl
        }
      }
      venue {
        city
        address
      }
    }
  }
}
"""

current_date = datetime.now()

formatted_date = {
    "year": current_date.year,
    "month": current_date.month,
    "day": current_date.day,
}

variables = {"first": 1, "startDate": {"after": formatted_date}}


def get_next_event() -> Event:
    data = GraphQLClient(variables=variables, query=query).get()
    result = data["data"]["events"]["nodes"][0]

    organizers_data = OrganizerData(
        nodes=[
            Organizer(title=node["title"])
            for node in result.get("organizers", {}).get("nodes", [])
        ]
    )
    events_categories_list = [
        {"name": node["name"]}
        for node in result.get("events_categories", {}).get("nodes", [])
    ]
    featured_image = result.get("featured_image")
    venue_data = result.get("venue", {})

    event = Event(
        title=result["title"],
        duration=result["duration"],
        start_date=result["start_date"],
        end_date=result["end_date"],
        date=result["date"],
        all_day=result["all_day"],
        url=result["url"],
        link=result["link"],
        events_categories=events_categories_list,
        featured_image=featured_image,
        organizers=organizers_data,
        venue=Venue(city=venue_data.get("city"), address=venue_data.get("address")),
    )
    return event
