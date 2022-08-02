import abc
import math

from dataclasses import dataclass
from typing import Any, Tuple

from uttlv.error import LengthSizeException, ValidationException


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
    value_min_size: int = None
    # Max number of bytes allowed to encode a length
    max_allowed_length_size: int = 8
    # Max size that a length value can be encoded into. If None, it is calculated automatically.
    length_size: int = None

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

    def encode_length(self, value: bytes) -> bytes:
        """Encodes the length of this tag into a byte array.

        :param value: encoded value array
        :returns: array with length encoded.
        """
        required_len_size = math.ceil(len(value).bit_length() / 8)
        # To avoid a big number of data, we set a limit to the maximum length that we can encode.
        if required_len_size > self.max_allowed_length_size:
            raise LengthSizeException(
                f"Max allowed value length is {2**(8*self.max_allowed_length_size - 1)-1} bytes, "
                f"given value is {len(value)} bytes"
            )

        # If nothing was set, it means we want to calculate the actual value we need.
        if not self.length_size:
            # For this, if the value if less than 128, we use only one byte to encode it.
            if len(value) < 128:
                return len(value).to_bytes(1, byteorder=self.endian)
            # If greater than 128, we set the first bit to 1 (by adding 0x80) and use the rest of 
            # the first byte to indicate how many bytes we need for the length.
            # The actual length will be encoded in the rest of the required len size.
            return bytes((0x80 + required_len_size,)) + len(value).to_bytes(
                required_len_size, byteorder=self.endian
            )

        # If we set an actual value for the length size, then we use it even if it more than
        # necessary. If it's less, than we abort it and tell the user about it.
        if self.length_size < required_len_size:
            raise LengthSizeException(
                f"{value} takes up {required_len_size} bytes, "
                f"but length_size was defined as {self.length_size}"
            )

        return len(value).to_bytes(self.length_size, byteorder=self.endian)

    @abc.abstractmethod
    def encode_value(self, value: Any) -> bytes:
        """Encodes value into a byte array.

        :param value: original value to be encoded.
        :returns: byte-array with encoded value.
        """
        pass

    def decode_length(self, data: bytes) -> Tuple(int, int):
        """Decodes value from an array.

        :param data: original array with value.
        :returns: Tuple with two values. First indicates the length size.
                  The second one is the actual length itself.
        """
        # If we don't have a required length size, we need to get this information from the
        # array itself, so we use the inverse logic from the `:py:attr:BaseTag.encode_length` 
        # method
        len_size = self.length_size
        offset = 0
        if not len_size:
            len_size = 1 if data[0] < 0x80 else (data[0] - 0x80 + 1)
            # If we need more than 1 byte, than we need to skip the first one, since we just use it
            # to indicate how many bytes we need for the actual value.
            offset = 0 if len_size == 1 else 0

        # Decode the code from the array 
        length = int.from_bytes(data[offset:len_size], byteorder=self.endian)
        # return the values we found
        return (len_size, length)

    @abc.abstractmethod
    def decode_value(self, arr: bytes, length: int) -> Any:
        """Decodes array into a valid value.

        :param arr: byte-array with original value.
        :param length: actual length to be analysed. 
        :returns: decoded value.
        """
        pass
