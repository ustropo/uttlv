import pytest

from uttlv import TLV
from uttlv.tlv import TLVIterator

config = {
    0x01: {TLV.Config.Type: int, TLV.Config.Name: 'NUM_POINTS'},
    0x02: {TLV.Config.Type: int, TLV.Config.Name: 'IDLE_PERIOD'},
    0x03: {TLV.Config.Type: str, TLV.Config.Name: 'NAME'},
    0x04: {TLV.Config.Type: str, TLV.Config.Name: 'CITY'},
    0x05: {TLV.Config.Type: bytes, TLV.Config.Name: 'VERSION'},
    0x06: {TLV.Config.Type: bytes, TLV.Config.Name: 'DATA'},
    0x07: {TLV.Config.Type: TLV, TLV.Config.Name: 'RELATED'},
    0x08: {TLV.Config.Type: TLV, TLV.Config.Name: 'COMMENT'},
    0x09: {TLV.Config.Type: TLV, TLV.Config.Name: 'Empty'}
}


class TestIterate:
    """Test iteration trough top-level tags."""

    def setup_class(self):
        TLV.set_global_tag_map(config)

    def setup_method(self):
        self.tlv = TLV(len_size=2)

        '''int object type'''
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0xA9]
        self.tlv.parse_array(arr)

        '''str object type'''
        arr = [0x02, 0x00, 0x04, 0x30, 0x31, 0x32, 0x33]
        self.tlv.parse_array(arr)

        '''tlv object type'''
        arr = [0x08, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        self.tlv.parse_array(arr)

    def test_iterator_available(self):
        """Test if correct iterator available"""
        it = iter(self.tlv)

        assert isinstance(it, TLVIterator)

    def test_iteration_trough_objects(self):
        """Test iteration trough parsed values"""
        it = iter(self.tlv)

        assert next(it) == 1
        assert next(it) == 2
        assert next(it) == 8

    def test_iteration_raise_exception(self):
        """Test out of index iteration """
        it = iter(self.tlv)

        assert next(it) == 1
        assert next(it) == 2
        assert next(it) == 8

        with pytest.raises(StopIteration):
            next(it)

    def test_iteration_empty_raise_exception(self):
        """Test empty class"""
        tlv = TLV(len_size=2)
        it = iter(tlv)

        with pytest.raises(StopIteration):
            next(it)
