from dataclasses import dataclass
from typing import Any, Tuple

from uttlv.tlv.base_tlv import BaseTLV


@dataclass
class BytesTLV(BaseTLV):
    """A TLV object with Bytes as its type."""

    def _convert_value(self, new_value: bytes) -> Tuple[Any, bytes]:
        if not isinstance(new_value, bytes):
            raise TypeError(f"This TLV only accepts 'bytes', received {type(new_value).__name__}")

        # No need to convert anything. The real and converted value are the same.
        return new_value, new_value
