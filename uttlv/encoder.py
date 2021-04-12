from __future__ import annotations
from binascii import hexlify


class DefaultEncoder(object):

    def default(self, obj):
        try:
            return obj.to_byte_array()
        except:
            raise TypeError('Invalid type')
    
    def to_string(self, obj, offset=0, use_names=False):
        try:
            return obj.tree(offset + obj.indent, use_names)
        except:
            pass
        return str(obj)

    def parse(self, obj, cls=None):
        try:
            cls.parse_array(obj)
            return cls
        except:
            pass
        return obj


class IntEncoder(DefaultEncoder):

    def default(self, obj):
        if isinstance(obj, int):
            return obj.to_bytes(4, byteorder='big')
        return super().default(obj)

    def parse(self, obj, cls=None):
        return int.from_bytes(obj, byteorder='big')


class AsciiEncoder(DefaultEncoder):

    def default(self, obj):
        if isinstance(obj, str):
            return obj.encode('ascii')
        return super().default(obj)

    def parse(self, obj, cls=None):
        return obj.decode('ascii')


class BytesEncoder(DefaultEncoder):

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj
        return super().default(obj)

    def to_string(self, obj, offset=0, use_names=False):
        return str(hexlify(obj), 'ascii')

    def parse(self, obj, cls=None):
        return obj


class Utf8Encoder(DefaultEncoder):

    def default(self, obj):
        if isinstance(obj, str):
            return obj.encode('utf8')
        return super().default(obj)

    def parse(self, obj, cls=None):
        return obj.decode('utf8')


class Utf16Encoder(DefaultEncoder):

    def default(self, obj):
        if isinstance(obj, str):
            return obj.encode('utf16')
        return super().default(obj)

    def parse(self, obj, cls=None):
        return obj.decode('utf16')


class Utf32Encoder(DefaultEncoder):

    def default(self, obj):
        if isinstance(obj, str):
            return obj.encode('utf32')
        return super().default(obj)

    def parse(self, obj, cls=None):
        return obj.decode('utf32')
