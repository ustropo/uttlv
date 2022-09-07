import pytest

from uttlv.const import Endianness
from uttlv.error import LengthException


class TestIntTag:
    """Tests for IntTag class."""

    def test_creation(self, int_tag):
        """Test basic class creation and basic attributes are correct."""
        assert int_tag.code == 0x02
        assert int_tag.name == "NUM_POINTS"
        assert int_tag.tag_type == int
        assert int_tag.raise_if_invalid
        assert int_tag.endian == Endianness.BIG
        assert int_tag.max_allowed_length_size == 2
        assert int_tag.bytes_length == 0
        assert not int_tag.should_validate
        assert not int_tag.value_min_size
        assert not int_tag.length_size
        assert not int_tag.max_value
        assert not int_tag.min_value

    def test_encode_value(self, int_tag):
        """Test int encode method."""
        real_value = b"\x0A"
        converted_value = 10

        assert int_tag.encode_value(converted_value) == real_value

    def test_decode_value(self, int_tag):
        """Test int decode method."""
        real_value = b"\x0A"
        converted_value = 10

        assert int_tag.decode_value(real_value) == converted_value

    def test_encode_length(self, int_tag):
        """Test encode value length."""
        converted_value = 10
        real_value = b"\x00\x00\x00\x0A"

        int_tag.bytes_length = 4
        assert int_tag.encode_value(converted_value) == real_value

        converted_value = 260
        real_value = b"\x00\x00\x01\x04"
        assert int_tag.encode_value(converted_value) == real_value

        # not enough size
        int_tag.bytes_length = 1
        with pytest.raises(LengthException) as exc:
            int_tag.encode_value(converted_value)
        assert str(exc.value) == "260 needs 2 bytes, but this tag accepts only 1"

    def test_encode_decode_endianness(self, int_tag):
        """Test with little endian"""
        int_tag.endian = Endianness.LITTLE
        int_tag.bytes_length = 4

        converted_value = 260
        real_value = b"\x04\x01\x00\x00"

        assert int_tag.encode_value(converted_value) == real_value
        assert int_tag.decode_value(real_value) == converted_value

    def test_validate_min_value(self, int_tag):
        """Test if min value is corrected validated."""
        converted_value = 10

        # min value is OK
        int_tag.min_value = 5
        msg = int_tag._validate_value(converted_value)
        assert not msg

        # min length is NOK
        int_tag.min_value = 15
        msg = int_tag._validate_value(converted_value)
        assert msg == f"The minimum value for this tag is {int_tag.min_value}"

    def test_validate_max_value(self, int_tag):
        """Test if max value is corrected validated."""
        converted_value = 10

        # max value is OK
        int_tag.max_value = 15
        msg = int_tag._validate_value(converted_value)
        assert not msg

        # max value is NOK
        int_tag.max_value = 2
        msg = int_tag._validate_value(converted_value)
        assert msg == f"The maximum value for this tag is {int_tag.max_value}"
