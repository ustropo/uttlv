from dataclasses import dataclass
from typing import Any


@dataclass
class TLVProtocol:
    """
    Class to represent a TLV (Tag-Length-Value) protocol.

    A protocol consists of a group of TLV objects, each of them representing an unique information.
    """

    tags: dict
    default_encoder: Any
    default_decoder: Any
    tag_size: int = 0
    length_size: int = 0
    allow_unknown_tags: bool = True
