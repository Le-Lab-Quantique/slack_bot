from src.utils import ExtendedEnum

from typing import Optional


class JobActionsId(ExtendedEnum):
    TITLE_ACTION = "job_title_"
    DESCRIPTION = "job_description_"
    LOCALIZATION = "job_localization_"
    TYPE_OF_CONTRACT = "job_type_of_contract_"
    TYPE_OF_POST = "job_type_of_post_"
    PRESENCE = "job_presence_"
    COMPANY = "job_compagny_name_"
    CONTACT_EMAIL = "job_contact_email"
    APPLY_LINK = "job_apply_link"


class JobConfig:
    def __init__(
        self,
        label: str,
        action_id: JobActionsId,
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
