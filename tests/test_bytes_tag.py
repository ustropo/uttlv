import pytest

from uttlv.const import Endianness
from uttlv.error import LengthException


class TestBytesTag:
    """Tests for BytesTag class."""

    def test_creation(self, bytes_tag):
        """Test basic class creation and basic attributes are correct."""
        assert bytes_tag.code == 0x01
        assert bytes_tag.name == "DATA"
        assert bytes_tag.tag_type == "bytes"
        assert not bytes_tag.should_validate
        assert bytes_tag.raise_if_invalid
        assert bytes_tag.endian == Endianness.BIG
        assert not bytes_tag.value_min_size
        assert not bytes_tag.length_size
        assert bytes_tag.max_allowed_length_size == 2
        assert not bytes_tag.min_length
        assert not bytes_tag.max_length

    def test_encode_value(self, bytes_tag):
        """Test bytes encode method."""
        data = b"\x00\x01\x02"

        # The bytes tag does nothing with the value, so it should be the same
        assert bytes_tag.encode_value(data) == data

    def test_decode_value(self, bytes_tag):
        """Test bytes decode method."""
        data = b"\x00\x01\x02"

        # The bytes tag does nothing with the value, so it should be the same
        assert bytes_tag.decode_value(data, len(data)) == data

    def test_decode_value_invalid_length(self, bytes_tag):
        """Test if decode value raises an exception when invalid length."""
        data = b"\x01\x02\x03"

        with pytest.raises(LengthException) as exc:
            bytes_tag.decode_value(data, 10)
        assert "value should be" in str(exc)

    def test_validate_min_length(self, bytes_tag):
        """Test if min length is corrected validated."""
        data = b"\x01\x02\x03"

        # min length is OK
        bytes_tag.min_length = 1
        msg = bytes_tag._validate_value(data)
        assert not msg

        # min length is NOK
        bytes_tag.min_length = 10
        msg = bytes_tag._validate_value(data)
        assert msg == f"The minimum size for this tag is {bytes_tag.min_length}"

    def test_validate_max_length(self, bytes_tag):
        """Test if max length is corrected validated."""
        data = b"\x01\x02\x03"

        # min length is OK
        bytes_tag.max_length = 10
        msg = bytes_tag._validate_value(data)
        assert not msg

        # min length is NOK
        bytes_tag.max_length = 2
        msg = bytes_tag._validate_value(data)
        assert msg == f"The maximum size for this tag is {bytes_tag.max_length}"
