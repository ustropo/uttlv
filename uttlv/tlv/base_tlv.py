"""BaseTLV class with common methods used in all package."""

import abc
from dataclasses import dataclass
from typing import Any, Tuple

from uttlv.tag import BaseTag


@dataclass
class BaseTLV(abc.ABC):
    """Base class for TLV (Tag-Length-Value) object."""

    # Tag object that this object refer`s to
    tag: BaseTag
    # Original byte-array value
    _real_value: bytes = None
    # Decoded value - real representation
    _converted_value: Any = None

    @abc.abstractmethod
    def _convert_value(self, new_value: Any) -> Tuple[Any, bytes]:
        """Tries to encode/decode value.

        If `new_value` is of `bytes` type, it will try to decode it to the TLV associated type.
        If `new_value` is of another type, it will try to encode it to `bytes`.

        :params new_value: value that we are trying to set this TLV.
        :returns: a tuple with two values. First is the converted_value, with the type specified by
                  `:py:attr:BaseTLV.tag`. Second is the real_value, the value as encoded in bytes.
        :raises TypeError: invalid or unknown type for this TLV.
        """

    @property
    def value(self) -> Any:
        """
        Get value of the TLV object.

        :returns: :py:attr:`BaseTLV._converted_value` if available.
                  Otherwise, it returns  :py:attr:`BaseTLV._real_value`.
        """
        if self._converted_value is not None:
            return self._converted_value

        return self._real_value

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
        self._real_value, self._converted_value = self._convert_value(new_value)
