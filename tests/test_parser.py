import pytest

from uttlv import TLV

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


class TestParser:
    """Test array parser feature."""

    def setup_class(self):
        TLV.set_global_tag_map(config)

    def setup_method(self):
        self.tlv = TLV(len_size=2)
        self.vtlv = TLV()

    def test_single_int(self):
        """Test single int array parser."""
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x10]
        self.tlv.parse_array(arr)

        assert self.tlv[0x01] == 16

    def test_single_str(self):
        """Test single str array parser."""
        arr = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.tlv.parse_array(arr)

        assert self.tlv[0x03] == 'teste'

    def test_single_bytes(self):
        """Test single bytes array parser."""
        arr = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03]
        self.tlv.parse_array(arr)

        assert list(self.tlv[0x05]) == [1, 2, 3]

    def test_single_tlv(self):
        """Test a single tlv tag"""
        t = TLV(len_size=2)
        t[0x01] = 25
        arr = [0x07, 0x00, 0x07, 0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x19]
        self.tlv.parse_array(arr)
        # Check values
        assert self.tlv[0x07] == t

    def test_nested_int(self):
        """Test tlv object type"""
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        self.tlv.parse_array(arr)

        assert self.tlv[0x01] == 10
        assert self.tlv[0x02] == 255

    def test_nested_str(self):
        """Test nested string object"""
        arr = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x04, 0x00, 0x06, 0x6d, 0x61, 0x69, 0x73, 0x75, 0x6d]
        self.tlv.parse_array(arr)
        # Check values
        assert self.tlv[0x03] == 'teste'
        assert self.tlv[0x04] == 'maisum'

    def test_nested_byte(self):
        """Test nested bytes object"""
        arr = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03, 0x06, 0x00, 0x03, 0x05, 0x06, 0x07]
        self.tlv.parse_array(arr)
        # Check values
        assert list(self.tlv[0x05]) == [1, 2, 3]
        assert list(self.tlv[0x06]) == [5, 6, 7]

    def test_nested_tlv(self):
        """Test a nested tlv tag"""
        arr = [0x07, 0x00, 0x07, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0x20, 0x08, 0x00, 0x08, 0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.tlv.parse_array(arr)
        # Check value
        t1 = TLV(len_size=2)
        t1[0x02] = 32
        t2 = TLV(len_size=2)
        t2[0x03] = 'teste'
        # Assert
        assert self.tlv[0x07] == t1
        assert self.tlv[0x08] == t2
        
    def test_auto_len_single_int(self):
        """Test single int array parser."""
        arr = [0x01, 0x04, 0x00, 0x00, 0x00, 0x10]
        self.vtlv.parse_array(arr)

        assert self.vtlv[0x01] == 16

    def test_auto_len_single_str(self):
        """Test single str array parser."""
        arr = [0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.vtlv.parse_array(arr)

        assert self.vtlv[0x03] == 'teste'

    def test_auto_len_single_bytes(self):
        """Test single bytes array parser."""
        arr = [0x05, 0x03, 0x01, 0x02, 0x03]
        self.vtlv.parse_array(arr)

        assert list(self.vtlv[0x05]) == [1, 2, 3]

    def test_auto_len_single_tlv(self):
        """Test a single tlv tag"""
        t = TLV()
        t[0x01] = 25
        arr = [0x07, 0x07, 0x01, 0x04, 0x00, 0x00, 0x00, 0x19]
        self.vtlv.parse_array(arr)
        # Check values
        assert t == self.vtlv[0x07]

    def test_auto_len_nested_int(self):
        """Test tlv object type"""
        arr = [0x01, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x04, 0x00, 0x00, 0x00, 0xFF]
        self.vtlv.parse_array(arr)

        assert self.vtlv[0x01] == 10
        assert self.vtlv[0x02] == 255

    def test_auto_len_nested_str(self):
        """Test nested string object"""
        arr = [0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x04, 0x06, 0x6d, 0x61, 0x69, 0x73, 0x75, 0x6d]
        self.vtlv.parse_array(arr)
        # Check values
        assert self.vtlv[0x03] == 'teste'
        assert self.vtlv[0x04] == 'maisum'

    def test_auto_len_nested_byte(self):
        """Test nested bytes object"""
        arr = [0x05, 0x03, 0x01, 0x02, 0x03, 0x06, 0x03, 0x05, 0x06, 0x07]
        self.vtlv.parse_array(arr)
        # Check values
        assert list(self.vtlv[0x05]) == [1, 2, 3]
        assert list(self.vtlv[0x06]) == [5, 6, 7]

    def test_auto_len_nested_tlv(self):
        """Test a nested tlv tag"""
        arr = [0x07, 0x06, 0x02, 0x04, 0x00, 0x00, 0x00, 0x20,
               0x08, 0x07, 0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.vtlv.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = 'teste'
        # Assert
        assert self.vtlv[0x07] == t1
        assert self.vtlv[0x08] == t2

    def test_auto_len_nested_tlv_with_empty(self):
        """Test a nested tlv tag"""
        arr = [0x07, 0x06, 0x02, 0x04, 0x00, 0x00, 0x00, 0x20, 0x08, 0x07,
               0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x09, 0x02, 0x01, 0x00]
        self.vtlv.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = 'teste'
        # Assert
        assert self.vtlv[0x07] == t1
        assert self.vtlv[0x08] == t2
        assert self.vtlv[0x09] == TLV()

    def test_auto_len_single_long_str(self):
        """Test single str array parser."""
        v = b'teste' * (2 ** 15 + 5)
        arr = b'\x03' + self.vtlv.encode_length(v) + v
        self.vtlv.parse_array(arr)

        assert v.decode('ascii') == self.vtlv[0x03]
