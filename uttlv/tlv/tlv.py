"""BaseTLV class with common methods used in all package."""
from dataclasses import dataclass
from typing import Any

from uttlv.tag import BaseTag


@dataclass
class TLV:
    """Base class for TLV (Tag-Length-Value) object."""

    # Tag object that this object refers to
    tag: BaseTag
    # Original byte-array value
    _real_value: bytes = None
    # Decoded value - real representation
    _converted_value: Any = None

    @property
    def value(self) -> Any:
        """
        Get value of the TLV object.

        :returns: :py:attr:`BaseTLV._converted_value` if available.
                  Otherwise, it returns  :py:attr:`BaseTLV._real_value`.
        """
        return self._real_value if self._converted_value is None else self._converted_value

    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Set new_value as this TLV object's value.

        If `new_value` is `bytes`, then the value is set to :py:attr:`BaseTLV._real_value`. If this
        tag has a known type, and a tag is available, it is then converted to that particular
        type and the value set to :py:attr:`BaseTLV._converted_value`.

        If `new_value` is of any type other than `bytes`, and a tag is available, then it tries
        to encode the value into `bytes` and set it to :py:attr:`BaseTLV._real_value`. The original
        value is set to :py:attr:`BaseTLV._converted_value`.

        :param new_value: new value of this TLV object
        """
        # TODO: add lazy conversion
        if isinstance(new_value, bytes):
            real_value = new_value
            converted_value = self.tag.decode_value(new_value)
        elif isinstance(new_value, self.tag.tag_type):
            real_value = self.tag.encode_value(new_value)
            converted_value = new_value
        else:
            raise TypeError(
                f"Invalid type {new_value.__class__.__name__}. Expected bytes or {self.tag.tag_type.__name__}"
            )

        self._real_value = real_value
        self._converted_value = converted_value
