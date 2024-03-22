from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EventCategory:
    name: str


@dataclass
class FeaturedImageNode:
    source_url: str


@dataclass
class Venue:
    city: str
    address: str


@dataclass
class Organizer:
    title: str


@dataclass
class Event:
    title: str
    duration: str
    start_date: str
    end_date: str
    date: str
    all_day: bool
    url: Optional[str]
    link: str
    events_categories: List[EventCategory]
    featured_image: Optional[FeaturedImageNode]
    organizers: Optional[List[Organizer]]
    venue: Venue
