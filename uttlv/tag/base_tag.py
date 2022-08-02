import abc
from dataclasses import dataclass
from typing import Any

from uttlv.error import ValidationException


@dataclass
class BaseTag(abc.ABC):
    """
    Class that represents the basic tag`s fields.

    A Tag is a class to configure a TLV tag with values such as code, type, etc.
    """

    code: int  # Tag's code
    name: str  # Tag's name
    tag_type: str  # Type of the value of the tag
    should_validate: bool = False  # Whether or not to validate the tag's value
    raise_if_invalid: bool = True  # If validation fails and this is True, it raises an exception
    endian: str = "big"  # Byte endianness to be used in encode and decode methods
    # Min size that value will occupy when encoded. If 0 or None, it is the minimum possible.
    value_min_size: int = 0

    def __validate_value(self, value: Any) -> str:
        """
        Validate if tag value is correct.

        :param value: value to be validated.
        :returns: a message with the validation error, if any.
        """
        return None

    def validate(self, value: Any) -> bool:
        """
        Validate if tag value is correct.

        :param value: value to be validated.
        :returns: True if valid. If `:py:attr:BaseTag.raise_if_invalid` is True, then an exception
                  is raised if the validation fails.
        """
        if not self.should_validate:
            return True

        error_msg = self.__validate_value(value)
        if error_msg and self.raise_if_invalid:
            raise ValidationException(error_msg)

        return error_msg is not None

    @abc.abstractmethod
    def encode_value(self, value: Any) -> bytes:
        """Encodes value into a byte array.

        :param value: original value to be encoded.
        :returns: byte-array with encoded value.
        """
        pass

    @abc.abstractmethod
    def decode_value(self, arr: bytes) -> Any:
        """Decodes array into a valid value.

        :param arr: byte-array with original value.
        :returns: decoded value.
        """
        pass
