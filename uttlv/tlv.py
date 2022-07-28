from dataclasses import dataclass
from typing import Any


@dataclass
class BaseTLV:
    """Base class for TLV (Tag-Length-Value) object."""

    tag: int
    name: str = None
    length: int = None
    real_value: bytes = None
    converted_value: Any = None
    tag_type: type = bytes.__class__

    @property
    def value(self) -> Any:
        """
        Get value of the TLV object.

        :returns: :py:attr:`BaseTLV.converted_value` if available.
                  Otherwise, it returns  :py:attr:`BaseTLV.real_value`.
        """
        if self.converted_value is not None:
            return self.converted_value

        return self.real_value

    # TODO: add value encoder/decoder param
    def set_value(self, new_value: Any) -> None:
        """
        Set new_value as this TLV object's value.

        If `new_value` is `bytes`, then the value is set to :py:attr:`BaseTLV.real_value`. If this
        tag has a known type, and a decoder is available, it is then converted to that particular
        type and the value set to :py:attr:`BaseTLV.converted_value`.

        If `new_value` is of any type other than `bytes`, and an encoder is available, then it tries
        to encode the value into `bytes` and set it to :py:attr:`BaseTLV.real_value`. The original
        value is set to :py:attr:`BaseTLV.converted_value`.

        If `skip_conversion` is `True`, then the encode / decode process is not executed.

        :param new_value: new value of this TLV object
        """
        pass
