from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    title: str
    contact_email: Optional[str]
