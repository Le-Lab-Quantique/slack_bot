from enum import Enum

from typing import Optional


class JobActionIds(Enum):
    TITLE_ACTION = "job_title-action"
    CONTACT_EMAIL = "job_contact_email-action"
    DESCRIPTION = "job_description-action"
    LOCALIZATION = "job_localization-action"
    TYPE_OF_CONTRACT = "job_type_of_contract-action"
    TYPE_OF_POST = "job_type_of_post-action"
    DESCRIPTION_FILE = "job_description_file-action"
    APPLY_LINK = "job_apply_link-action"
    COMPANY = "job_company-action"


class JobConfig:
    def __init__(
        self,
        label: str,
        action_id: JobActionIds,
        placeholder: str,
        options: Optional[list[dict]] = None,
        is_multiline: bool = False,
        is_optional: bool = False,
    ):
        self.label = label
        self.action_id = action_id.value
        self.placeholder = placeholder
        self.options = options or []
        self.is_multiline = is_multiline
        self.is_optional = is_optional
