from typing import Optional
from src.utils import ExtendedEnum
from src.slack.job.job_definition import JobConfig
from enum import Enum

from .modal_ids import ModalsCallbackId


class InputElementTypes(Enum):
    STATIC_SELECT = "static_select"
    PLAIN_TEXT_INPUT = "plain_text_input"


class PlainText:
    def __init__(self, text: str):
        self.type = "plain_text"
        self.text = text


class DropdownElement:
    def __init__(self, text: str, value: Optional[str] = None) -> None:
        self.text = PlainText(text)
        self.value = value or text


class InputConfig:
    def __init__(
        self,
        label: str,
        action_id: ExtendedEnum,
        placeholder: str,
        options: Optional[list[DropdownElement]] = None,
        is_multiline: bool = False,
        is_optional: bool = False,
    ):
        self.label = label
        self.action_id = action_id.value
        self.placeholder = placeholder
        self.options = options or []
        self.is_multiline = is_multiline
        self.is_optional = is_optional


class InputElement:
    def __init__(self, config: JobConfig, type: InputElementTypes):
        self.type = type.value
        self.action_id = config.action_id
        self.placeholder = PlainText(config.placeholder)


class StaticSelect(InputElement):
    def __init__(self, config: JobConfig):
        super().__init__(config, InputElementTypes.STATIC_SELECT)
        self.options = config.options or []


class PlainTextInput(InputElement):
    def __init__(self, config: JobConfig):
        super().__init__(config, InputElementTypes.PLAIN_TEXT_INPUT)
        if config.is_multiline:
            self.multiline = config.is_multiline


class Input:
    def __init__(self, config: JobConfig) -> None:
        self.type = "input"
        if config.options:
            self.element = StaticSelect(config)
        else:
            self.element = PlainTextInput(config)
        self.label = PlainText(config.label)
        self.optional = config.is_optional


class Modal:
    def __init__(
        self, modal_id: ModalsCallbackId, title: str, configs: list[InputConfig]
    ) -> None:
        self.type = "modal"
        self.callback_id = modal_id.value
        self.title = PlainText(title)
        self.close = PlainText("Close")
        self.submit = PlainText("Submit")
        self.blocks = [Input(config) for config in configs]
