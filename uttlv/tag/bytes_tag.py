"""Tag that handles byte-array content."""


from dataclasses import dataclass

from .base_tag import BaseTag


@dataclass
class BytesTag(BaseTag):
    """Class to handle byte-array tags."""

    min_length: int = None  # Min length valid for this array
    max_length: int = None  # Max length valid for this array
    tag_type: type = bytes

    def _validate_value(self, value: bytes) -> str:
        """Validate if tag value is correct.

        If `:py:attr:BytesTag.min_value` is set, checks if value's length is less than it.
        If `:py:attr:BytesTag.max_value` is set, checks if value's length is greater than it.

        :param value: value to be validated.
        :returns: an error message if validation fails, None otherwise
        """
        msg = ""
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
        # We check if the value of the array has the minimum we expect for it.
        self.validate(arr)
        # Nothing to do here.
        return arr
