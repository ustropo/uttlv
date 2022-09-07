import math
from dataclasses import dataclass
from typing import Any

from uttlv.error import LengthException

from .base_tag import BaseTag


@dataclass
class IntTag(BaseTag):
    """
    Class that represents an integer tag.
    """

    # Min value that this Tag can assume
    min_value: int = None
    # Max value that this Tag can assume
    max_value: int = None
    # How many bytes this value will assume in the byte array.
    # If 0 or None, this will use the minimum amount required to represent in bytes format
    bytes_length: int = 0
    # Base type for this tag
    tag_type: type = int

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

        # We check if we have enough room to encode this value
        required_len = math.ceil(value.bit_length() / 8)
        if self.bytes_length and 0 < self.bytes_length < required_len:
            raise LengthException(
                f"{value} needs {required_len} bytes, but this tag accepts only {self.bytes_length}"
            )

        # If bytes_length is 0 (or None), we use the minimum amount of bytes to encode it
        # Otherwise, just use the size its defined for this tag
        required_len = self.bytes_length or required_len
        return value.to_bytes(required_len, self.endian.value)

    def decode_value(self, arr: bytes) -> Any:
        value = int.from_bytes(arr, self.endian.value)
        self.validate(value)

        return value
