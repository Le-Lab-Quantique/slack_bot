from typing import Optional
from src.utils import ExtendedEnum


class ModalCallbackIds(ExtendedEnum):
    JOB = "modal-submit-job"


def builld_modal_information(modal_id: str, title: str) -> dict:
    return {
        "type": "modal",
        "callback_id": modal_id,
        "title": {"type": "plain_text", "text": title},
        "close": {"type": "plain_text", "text": "Close"},
        "submit": {"type": "plain_text", "text": "Submit"},
    }


def build_dropdown_list_option(text: str, value: Optional[str]) -> dict:
    return {
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True,
        },
        "value": value if value else text,
    }
