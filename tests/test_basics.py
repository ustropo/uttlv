from uttlv import TLV, EmptyTLV


class TestBasic:
    """Class to execute some basic tests over package."""

    def test_int_one(self, tag):
        """Test if a TLV object is corrected set to an array"""
        tag[0x01] = 10
        # Create an array
        v = list(tag.to_byte_array())
        exp = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A]
        # Check value
        assert exp == v

    def test_int_nested(self, tag):
        """Test more than one int tag in an array."""
        tag[0x01] = 10
        tag[0x02] = 255
        # Create array
        v = list(tag.to_byte_array())
        exp = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        # Check value
        assert exp == v

    def test_str_one(self, tag):
        """Test string tag"""
        tag[0x03] = "teste"
        # Create array
        v = list(tag.to_byte_array())
        exp = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        # Check value
        assert exp == v

    def test_str_nested(self, tag):
        """Test string tag"""
        tag[0x03] = "teste"
        tag[0x04] = "maisum"
        # Create array
        v = list(tag.to_byte_array())
        exp = [
            0x03,
            0x00,
            0x05,
            0x74,
            0x65,
            0x73,
            0x74,
            0x65,
            0x04,
            0x00,
            0x06,
            0x6D,
            0x61,
            0x69,
            0x73,
            0x75,
            0x6D,
        ]
        # Check value
        assert exp == v

    def test_bytes_one(self, tag):
        """Test array of bytes tag"""
        tag[0x05] = bytes([1, 2, 3])
        # Create array
        v = list(tag.to_byte_array())
        exp = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03]
        # Check value
        assert exp == v

    def test_bytes_nested(self, tag):
        """Test array of bytes tag"""
        tag[0x05] = bytes([1, 2, 3])
        tag[0x06] = bytes([5, 6, 7])
        # Create array
        v = list(tag.to_byte_array())
        exp = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03, 0x06, 0x00, 0x03, 0x05, 0x06, 0x07]
        # Check value
        assert exp == v

    def test_tlv_one(self, tag):
        """Test a TLV tag object"""
        t = TLV(len_size=2)
        t[0x01] = 25
        tag[0x07] = t
        # Create array
        v = list(tag.to_byte_array())
        exp = [0x07, 0x00, 0x07, 0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x19]
        # Check value
        assert exp == v

    def test_tlv_nested(self, tag):
        """Test multiple tlv tag object"""
        t1 = TLV(len_size=2)
        t1[0x02] = 32
        t2 = TLV(len_size=2)
        t2[0x03] = "teste"
        tag[0x07] = t1
        tag[0x08] = t2
        # Create array
        v = list(tag.to_byte_array())
        exp = [
            0x07,
            0x00,
            0x07,
            0x02,
            0x00,
            0x04,
            0x00,
            0x00,
            0x00,
            0x20,
            0x08,
            0x00,
            0x08,
            0x03,
            0x00,
            0x05,
            0x74,
            0x65,
            0x73,
            0x74,
            0x65,
        ]
        # Check value
        assert exp == v

    def test_empty(self):
        """Test empty TLV object"""
        t = EmptyTLV(0x08, len_size=2)
        # Create array
        v = list(t.to_byte_array())
        exp = [0x08, 0x00, 0x00]
        # Check value
        assert exp == v

    def test_key_name(self, apply_global_map):
        """Test access by key name."""
        t = TLV()
        t["NUM_POINTS"] = 10

        assert t[1] == 10

    def test_attribute(self, apply_global_map):
        """Test access by attribute name."""
        t = TLV()
        t["NUM_POINTS"] = 10

        assert t.NUM_POINTS == 10

    def test_auto_len_single_byte(self, auto_len_tag):
        auto_len_tag[0x00] = b"1"
        exp = b"\x00\x01\x31"

        assert exp == auto_len_tag.to_byte_array()

    def test_auto_len_double_byte(self, auto_len_tag):
        auto_len_tag[0x01] = bytes(c % 256 for c in range(2**7 + 23))
        exp = b"\1\x81\x97" + auto_len_tag[0x01]

        assert exp == auto_len_tag.to_byte_array()

    def test_auto_len_triple_byte(self, auto_len_tag):
        auto_len_tag[0x02] = bytes(c % 256 for c in range(2**15 + 23))
        exp = b"\2\x82\x80\x17" + auto_len_tag[0x02]

        assert exp == auto_len_tag.to_byte_array()

    def test_auto_len_multiple_sizes(self, auto_len_tag):
        auto_len_tag[0x00] = b"1"
        auto_len_tag[0x01] = bytes(c % 256 for c in range(2**7 + 23))
        auto_len_tag[0x02] = bytes(c % 256 for c in range(2**15 + 23))
        exp = b"\0\1\x31\1\x81\x97" + auto_len_tag[0x01] + b"\2\x82\x80\x17" + auto_len_tag[0x02]

        assert exp == auto_len_tag.to_byte_array()
