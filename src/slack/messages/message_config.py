from dataclasses import dataclass
from typing import Optional


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
