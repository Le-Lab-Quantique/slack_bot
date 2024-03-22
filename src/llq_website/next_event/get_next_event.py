from datetime import datetime

from src.llq_website.client.graphql_client import GraphQLClient

from .next_event_types import Event

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
    return Event(**(data["data"]["events"]["nodes"][0]))
