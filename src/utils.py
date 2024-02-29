from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls) -> list:
        return [c.value for c in cls]
