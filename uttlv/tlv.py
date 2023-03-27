from __future__ import annotations

import enum
import math
from binascii import hexlify
from typing import Any, Dict

from .encoder import (
    BytesEncoder,
    DefaultEncoder,
    IntEncoder,
    FloatEncoder,
    NestedEncoder,
    Utf8Encoder,
)


class TLV:
    """
    Class that represents a TLV (tag-length-value) object.

    More: https://en.wikipedia.org/wiki/Type-length-value

    If you want to parse the values to real type instead of seeing
    as byte array, set the tag_map attribute with a dict:
        {
            <tag value>: <class name>,
            <tag value>: <class name>,
            ...
        }

        where:
            tag value is the int tag value.
            class name is the name of the class that represents the type
                of the value.
    """

    Config = enum.Enum("Config", "Type Name")
    _global_tag_map = {}

    def __init__(self, indent=4, tag_size=1, len_size=None, endian="big"):
        """
        :args:
            indent: How many spaces to use in tree() method
            tag_size: How many bytes a tag will contain in the array
            len_size: How many bytes the length info will occupy in the final
                        array, None (default) for automatically determine per
                        field
        """
        super().__init__()
        self.indent = indent
        self.tag_size = tag_size
        self.len_size = len_size
        self.endian = endian
        self._items = {}
        self._local_tag_map = None

    @property
    def tag_map(self) -> Dict:
        return self._local_tag_map or TLV._global_tag_map

    def __setitem__(self, key, value):
        real_key = self.__getkey__(key)
        self.check_key(real_key)
        self.check_value(value)
        self._items[real_key] = value

    def __getitem__(self, key):
        real_key = self.__getkey__(key)
        return self._items[real_key]

    def __getkey__(self, key):
        """Get real tag from a given string"""
        if isinstance(key, int):
            return key
        if isinstance(key, str):
            for tag, config in self.tag_map.items():
                name = config.get(TLV.Config.Name)
                if name and name == key:
                    return tag
            raise AttributeError(f"Key {key} not found")
        # Invalid key type
        raise KeyError(f"Invalid key {str(key)}")

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __eq__(self, other):
        if not isinstance(other, TLV):
            return False

        return self.to_byte_array() == other.to_byte_array()

    def __hash__(self):
        return hash(self.to_byte_array())

    def __iter__(self):
        return TLVIterator(self)

    def _new_equivalent_tlv(self) -> TLV:
        """Creates a new TLV object with the same decode settings as self.

        Useful for parsing nested structures.
        """
        return TLV(self.indent, self.tag_size, self.len_size, self.endian)

    @classmethod
    def set_tag_map(cls, tag_map: Dict) -> None:
        """Set a tag map globally for all classes (DEPRECATED, please use set_global_tag_map)

        :args:
            map: dict with keys names
        """
        cls.set_global_tag_map(tag_map)

    @classmethod
    def set_global_tag_map(cls, tag_map: Dict) -> None:
        """Set a tag map globally for all classes

        :args:
            map: dict with keys names
        """
        # Check if the map has correct types
        al_types = ALLOWED_TYPES.keys()
        for tag, config in tag_map.items():
            if not isinstance(config, dict):
                raise TypeError("Invalid tag config type")
            tag_config = config.get(TLV.Config.Type, "")
            if tag_config not in al_types:
                raise AttributeError(f"Invalid tag type {tag_config} for {tag} -> {config}")
        cls._global_tag_map = tag_map

    def set_local_tag_map(self, tag_map: Dict) -> None:
        """Set a class-instance-specific tag map.

        :args:
            map: tag map to set class instance to.
        """
        self._local_tag_map = tag_map

        # Iterate through any nested tag maps
        for index, cfg in tag_map.items():
            tg_type = cfg.get(TLV.Config.Type)
            if tg_type is not None and type(tg_type) is dict:
                if index not in self._items:
                    self._items[index] = self._new_equivalent_tlv()
                self._items[index].set_local_tag_map(tg_type)

    def check_key(self, key: int) -> bool:
        """Check if key is valid is inside limits.

        :args:
            key: key int value.
        """
        if not isinstance(key, int) or (key < 0 or key >= 2**(self.tag_size*8)):
            raise TypeError("Invalid key format.")
        return True

    def check_value(self, value: Any[TLV, str, int, bytes]) -> bool:
        """Check if value class is a valid one.

        :args:
            value: value to be inserted.
        """
        if not any(isinstance(value, t) for t in ALLOWED_TYPES):
            raise TypeError(f"Invalid value type format {type(value)}.")
        return True

    def encode_length(self, value: bytes) -> bytes:
        """Translate the length of value into an array."""
        required_len_size = math.ceil(len(value).bit_length() / 8)
        if required_len_size > 16:
            raise AttributeError(
                f"Max allowed value length is {2**(8*15)-1} bytes, "
                f"given value is {len(value)} bytes"
            )

        if not self.len_size:
            if len(value) < 128:
                return len(value).to_bytes(1, byteorder=self.endian)

            return bytes((0x80 + required_len_size,)) + len(value).to_bytes(
                required_len_size, byteorder=self.endian
            )

        if self.len_size < required_len_size:
            raise ValueError(
                f"{value} takes up {required_len_size} bytes, "
                f"but len_size was defined as {self.len_size}"
            )

        return len(value).to_bytes(self.len_size, byteorder=self.endian)

    def to_byte_array(self) -> bytes:
        """Translate all keys and values into an array of bytes."""
        data = bytes()
        for tag, value in self._items.items():
            formatter = ALLOWED_TYPES.get(type(value))
            formatted_value = formatter().default(value)
            # Create array
            data += int(tag).to_bytes(self.tag_size, byteorder=self.endian)
            data += self.encode_length(formatted_value)
            data += formatted_value
        return data

    def tree(self, offset: int = 0, use_names: bool = False, show_size: bool = False) -> str:
        """Print a tree view of the object."""
        tree_str = "" if offset == 0 else "\r\n"
        for tag, value in self._items.items():
            encoder = ALLOWED_TYPES.get(type(value))
            encoded_value = encoder().to_string(value, offset, use_names)
            # Create line
            encoded_tag = str(
                hexlify(int(tag).to_bytes(self.tag_size, byteorder=self.endian)), "ascii"
            )
            if use_names:
                tag_map = self.tag_map.get(tag, {})
                name = tag_map.get(TLV.Config.Name, None)
                encoded_tag = name or encoded_tag

            if(len(encoded_value) > 300):
                encoded_value = "*trimmed*"

            if show_size:
                formatted_value = encoder().default(value)
                tree_str += f'{" " * offset}{encoded_tag} (len:{len(formatted_value)}):{encoded_value}\r\n'
            else:
                tree_str += f'{" " * offset}{encoded_tag}: {encoded_value}\r\n'
        return tree_str

    def decode_len_size(self, data: bytes) -> int:
        if data[0] < 0x80:
            return 1
        return data[0] - 0x80 + 1

    def parse_array(self, data: Any[list, bytes]) -> bool:
        """Parse a byte array into a TLV object"""
        if isinstance(data, list):
            data = bytes(data)
        elif not isinstance(data, bytes):
            raise TypeError("Data must be bytes type.")
        # Check size
        min_len_size = self.len_size or 1
        min_size = min_len_size + self.tag_size
        if len(data) < min_size:
            raise AttributeError(f"Data must be at least {min_size} bytes long")
        # Start parsing
        aux = data
        while len(aux) > min_size:
            # Tag value
            tag = int.from_bytes(aux[: self.tag_size], byteorder=self.endian)
            # Len value
            aux = aux[self.tag_size :]
            len_size = self.len_size or self.decode_len_size(aux)
            offset = 0 if len_size == 1 else 1
            length = int.from_bytes(aux[offset:len_size], byteorder=self.endian)
            # Value
            aux = aux[len_size:]
            value = aux[:length]
            # Next value
            aux = aux[length:]
            # Check if tag has any parser
            tg_cfg = self.tag_map.get(tag)
            if tg_cfg is not None:
                tg_type = tg_cfg.get(TLV.Config.Type)
                if tg_type is not None:
                    # *Ideally* we would include this in ALLOWED_TYPES,
                    # but this is the easiest way I can think of
                    # to pass in the tag map config at the same time.
                    if type(tg_type) is dict:
                        value = NestedEncoder(tg_type).parse(value, self._new_equivalent_tlv())
                    else:
                        formatter = ALLOWED_TYPES.get(tg_type)
                        if formatter is not None:
                            formatter_instance = formatter(self.endian)
                            value = formatter_instance.parse(value, self._new_equivalent_tlv())
            # Set value
            self[tag] = value
        # Done parsing
        return True


class EmptyTLV(TLV):
    """Empty TLV"""

    def __init__(self, tag: int, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag

    def __setitem__(self, key, value):
        raise TypeError("Invalid argument")

    def to_byte_array(self) -> bytes:
        value = int(self.tag).to_bytes(self.tag_size, byteorder=self.endian)
        len_size = self.len_size or 1
        value += int(0).to_bytes(len_size, byteorder=self.endian)
        return value

    def tree(self, offset: int = 0, use_names: bool = False) -> str:
        tree_str = "" if offset == 0 else "\r\n"
        tag = str(hexlify(int(self.tag).to_bytes(self.tag_size, byteorder=self.endian)), "ascii")
        if use_names:
            tag_map = TLV.tag_map.get(self.tag, {})
            name = tag_map.get("name", None)
            tag = name or tag
        tree_str += f'{" " * offset}{tag}\r\n'
        return tree_str


class TLVIterator:
    """Iterator class"""

    def __init__(self, tlv: TLV):
        self._tlv = tlv
        self._it = iter(self._tlv._items)

    def __next__(self):
        """Returns the next value from items dictionary"""
        return next(self._it)


ALLOWED_TYPES = {
    TLV: DefaultEncoder,
    int: IntEncoder,
    float: FloatEncoder,
    bytes: BytesEncoder,
    str: Utf8Encoder,
}
