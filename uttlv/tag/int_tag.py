from dataclasses import dataclass
from typing import Any

from .base_tag import BaseTag


@dataclass
class IntTag(BaseTag):
    """
    Class that represents an integer tag.
    """

    min_value: int = None  # Min value that this Tag can assume
    max_value: int = None  # Max value that this Tag can assume
    bytes_length: int = 4  # How many bytes this value will assume in the byte array
    tag_type: type = int  # Base type for this tag

    def _validate_value(self, value: int) -> str:
        """Validate if tag value is correct.

        If `:py:attr:IntTag.min_value` is set, checks if value is greater or equal then it.
        If `:py:attr:IntTag.max_value` is set, checks if value is less or equal then it.

        :param value: value to be validated.
        :returns: an error message if validation fails, None otherwise
        """
        msg = None
        if self.min_value is not None and value < self.min_value:
            msg = f"The minimum value for this tag is {self.min_value}"

        if self.max_value is not None and value > self.max_value:
            msg = f"The maximum value for this tag is {self.max_value}"

        return msg

    def encode_value(self, value: int) -> bytes:
        self.validate(value)

        return value.to_bytes(self.bytes_length, self.endian.value)

    def decode_value(self, arr: bytes) -> Any:
        value = int.from_bytes(arr, self.endian.value)
        self.validate(value)

        return value
