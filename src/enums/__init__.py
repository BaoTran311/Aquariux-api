from enum import Enum


class BaseEnum(str, Enum):
    """Base enum class that provides string representation functionality."""

    def __str__(self):
        return self.value
