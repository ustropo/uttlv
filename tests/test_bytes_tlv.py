import pytest


class TestBytesTLV:
    """Tests for BytesTLV class."""

    def test_convert_value(self, bytes_tlv):
        """Test if convert value is correct."""
        data = b"\x01\x02\x03"

        ret = bytes_tlv._convert_value(data)
        assert isinstance(ret, tuple)
        assert len(ret) == 2
        assert ret[0] == data
        assert ret[1] == data

    def test_convert_value_invalid_type(self, bytes_tlv):
        """Test convert value for invalid type."""
        data = 10

        with pytest.raises(TypeError) as exc:
            bytes_tlv._convert_value(data)

        assert str(exc.value) == "This TLV only accepts 'bytes', received int"
