from dataclasses import dataclass

from .base_tag import BaseTag


@dataclass
class BytesTag(BaseTag):
    """Class to handle byte-array tags."""

    min_length: int = None  # Min length valid for this array
    max_length: int = None  # Max length valid for this array
    tag_type: str = "bytes"

    def __validate_value(self, value: bytes) -> str:
        """Validate if tag value is correct.

        If `:py:attr:IntTag.min_value` is set, checks if value is greater or equal then it.
        If `:py:attr:IntTag.max_value` is set, checks if value is less or equal then it.

        :param value: value to be validated.
        :returns: an error message if validation fails, None otherwise
        """
        msg = None
        if self.min_length is not None and len(value) < self.min_length:
            msg = f"The minimum size for this tag is {self.min_length}"

        if self.max_length is not None and len(value) > self.max_length:
            msg = f"The maximum size for this tag is {self.max_length}"

        return msg

    def encode_value(self, value: bytes) -> bytes:
        self.validate(value)
        # Nothing to do here.
        return value

    def decode_value(self, arr: bytes) -> bytes:
        self.validate(arr)
        # Nothing to do here.
        return arr
