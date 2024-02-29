from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls) -> list:
        return list(map(lambda c: c.value, cls))
