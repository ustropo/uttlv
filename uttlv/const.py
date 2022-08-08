from enum import Enum


class Endianness(Enum):
    """Class to define the type of endianness to use in decode/encode processes."""

    BIG = "big"
    LITTLE = "little"
