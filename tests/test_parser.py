from uttlv import TLV


class TestParser:
    """Test array parser feature."""

    def test_single_int(self, tag):
        """Test single int array parser."""
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x10]
        tag.parse_array(arr)

        assert tag[0x01] == 16

    def test_int8(self, tag):
        """Test single int 8-bit array parser."""
        arr = [0x01, 0x00, 0x01, 0xad]
        tag.parse_array(arr)

        assert tag[0x01] == 0xad

    def test_int16(self, tag):
        """Test single int 16-bit array parser."""
        arr = [0x01, 0x00, 0x02, 0xde, 0xad]
        tag.parse_array(arr)

        assert tag[0x01] == 0xdead

    def test_int64(self, tag):
        """Test single int 64-bit array parser."""
        arr = [0x01, 0x00, 0x08, 0xde, 0xad, 0xbe, 0xef, 0xde, 0xad, 0xbe, 0xef]
        tag.parse_array(arr)

        assert tag[0x01] == 0xdeadbeefdeadbeef

    def test_little_end(self, tag_little):
        """Test single int array parser from little endian."""
        arr = [0x01, 0x04, 0x00, 0x10, 0x00, 0x00, 0x00]
        tag_little.parse_array(arr)

        assert tag_little[0x01] == 16

    def test_int8_little(self, tag_little):
        """Test single int 8-bit array parser from little endian."""
        arr = [0x01, 0x01, 0x00, 0xde]
        tag_little.parse_array(arr)

        assert tag_little[0x01] == 0xde

    def test_int16_little(self, tag_little):
        """Test single int 16-bit array parser from little endian."""
        arr = [0x01, 0x02, 0x00, 0xad, 0xde]
        tag_little.parse_array(arr)

        assert tag_little[0x01] == 0xdead

    def test_int64_little(self, tag_little):
        """Test single int 64-bit array parser from little endian."""
        arr = [0x01, 0x08, 0x00, 0xef, 0xbe, 0xad, 0xde, 0xef, 0xbe, 0xad, 0xde]
        tag_little.parse_array(arr)

        assert tag_little[0x01] == 0xdeadbeefdeadbeef

    def test_single_str(self, tag):
        """Test single str array parser."""
        arr = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        tag.parse_array(arr)

        assert tag[0x03] == "teste"

    def test_single_bytes(self, tag):
        """Test single bytes array parser."""
        arr = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03]
        tag.parse_array(arr)

        assert list(tag[0x05]) == [1, 2, 3]

    def test_single_tlv(self, tag):
        """Test a single tlv tag"""
        t = TLV(len_size=2)
        t[0x01] = 25
        arr = [0x07, 0x00, 0x07, 0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x19]
        tag.parse_array(arr)
        # Check values
        assert tag[0x07] == t

    def test_nested_int(self, tag):
        """Test tlv object type"""
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        tag.parse_array(arr)

        assert tag[0x01] == 10
        assert tag[0x02] == 255

    def test_nested_str(self, tag):
        """Test nested string object"""
        arr = [
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
        tag.parse_array(arr)
        # Check values
        assert tag[0x03] == "teste"
        assert tag[0x04] == "maisum"

    def test_nested_byte(self, tag):
        """Test nested bytes object"""
        arr = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03, 0x06, 0x00, 0x03, 0x05, 0x06, 0x07]
        tag.parse_array(arr)
        # Check values
        assert list(tag[0x05]) == [1, 2, 3]
        assert list(tag[0x06]) == [5, 6, 7]

    def test_nested_tlv(self, tag):
        """Test a nested tlv tag"""
        arr = [
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
        tag.parse_array(arr)
        # Check value
        t1 = TLV(len_size=2)
        t1[0x02] = 32
        t2 = TLV(len_size=2)
        t2[0x03] = "teste"
        # Assert
        assert tag[0x07] == t1
        assert tag[0x08] == t2

    def test_auto_len_single_int(self, auto_len_tag):
        """Test single int array parser."""
        arr = [0x01, 0x04, 0x00, 0x00, 0x00, 0x10]
        auto_len_tag.parse_array(arr)

        assert auto_len_tag[0x01] == 16

    def test_auto_len_single_str(self, auto_len_tag):
        """Test single str array parser."""
        arr = [0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        auto_len_tag.parse_array(arr)

        assert auto_len_tag[0x03] == "teste"

    def test_auto_len_single_bytes(self, auto_len_tag):
        """Test single bytes array parser."""
        arr = [0x05, 0x03, 0x01, 0x02, 0x03]
        auto_len_tag.parse_array(arr)

        assert list(auto_len_tag[0x05]) == [1, 2, 3]

    def test_auto_len_single_tlv(self, auto_len_tag):
        """Test a single tlv tag"""
        t = TLV()
        t[0x01] = 25
        arr = [0x07, 0x07, 0x01, 0x04, 0x00, 0x00, 0x00, 0x19]
        auto_len_tag.parse_array(arr)
        # Check values
        assert t == auto_len_tag[0x07]

    def test_auto_len_nested_int(self, auto_len_tag):
        """Test tlv object type"""
        arr = [0x01, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x04, 0x00, 0x00, 0x00, 0xFF]
        auto_len_tag.parse_array(arr)

        assert auto_len_tag[0x01] == 10
        assert auto_len_tag[0x02] == 255

    def test_auto_len_nested_str(self, auto_len_tag):
        """Test nested string object"""
        arr = [
            0x03,
            0x05,
            0x74,
            0x65,
            0x73,
            0x74,
            0x65,
            0x04,
            0x06,
            0x6D,
            0x61,
            0x69,
            0x73,
            0x75,
            0x6D,
        ]
        auto_len_tag.parse_array(arr)
        # Check values
        assert auto_len_tag[0x03] == "teste"
        assert auto_len_tag[0x04] == "maisum"

    def test_auto_len_nested_byte(self, auto_len_tag):
        """Test nested bytes object"""
        arr = [0x05, 0x03, 0x01, 0x02, 0x03, 0x06, 0x03, 0x05, 0x06, 0x07]
        auto_len_tag.parse_array(arr)
        # Check values
        assert list(auto_len_tag[0x05]) == [1, 2, 3]
        assert list(auto_len_tag[0x06]) == [5, 6, 7]

    def test_auto_len_nested_tlv(self, auto_len_tag):
        """Test a nested tlv tag"""
        arr = [
            0x07,
            0x06,
            0x02,
            0x04,
            0x00,
            0x00,
            0x00,
            0x20,
            0x08,
            0x07,
            0x03,
            0x05,
            0x74,
            0x65,
            0x73,
            0x74,
            0x65,
        ]
        auto_len_tag.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = "teste"
        # Assert
        assert auto_len_tag[0x07] == t1
        assert auto_len_tag[0x08] == t2

    def test_auto_len_nested_tlv_with_empty(self, auto_len_tag):
        """Test a nested tlv tag"""
        arr = [
            0x07,
            0x06,
            0x02,
            0x04,
            0x00,
            0x00,
            0x00,
            0x20,
            0x08,
            0x07,
            0x03,
            0x05,
            0x74,
            0x65,
            0x73,
            0x74,
            0x65,
            0x09,
            0x02,
            0x01,
            0x00,
        ]
        auto_len_tag.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = "teste"
        # Assert
        assert auto_len_tag[0x07] == t1
        assert auto_len_tag[0x08] == t2
        assert auto_len_tag[0x09] == TLV()

    def test_auto_len_single_long_str(self, auto_len_tag):
        """Test single str array parser."""
        v = b"teste" * (2**15 + 5)
        arr = b"\x03" + auto_len_tag.encode_length(v) + v
        auto_len_tag.parse_array(arr)

        assert v.decode("ascii") == auto_len_tag[0x03]

    def test_auto_len_multi_byte_read(self, auto_len_tag):
        """Test auto length decoder with multi-byte length"""
        arr = [0x01, 0x81, 0x01, 0x01, 0x02, 0x01, 0x02]
        auto_len_tag.parse_array(arr)
        assert auto_len_tag[0x01] == 0x01
        assert auto_len_tag[0x02] == 0x02
