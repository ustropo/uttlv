import pytest

from uttlv.tlv import TLV


class TestTLV:
    def test_get_value(self, bytes_tag):
        """Test if method value property is working."""
        converted = 10
        real = b"\x0A"
        # TODO: change this to unknown tag
        bt = TLV(bytes_tag, _real_value=real)

        # It should return real value
        assert bt.value == real

        # It should return converted value
        bt = TLV(bytes_tag, _real_value=real, _converted_value=converted)
        assert bt.value == converted

    def test_set_value_with_converted(self, int_tag):
        """Test to see if setter works with converted value."""
        converted = 10
        real = b"\x0A"

        bt = TLV(int_tag)
        assert not bt.value

        bt.value = converted
        assert bt.value == converted
        assert bt._converted_value == converted
        assert bt._real_value == real

    def test_set_value_with_real(self, int_tag):
        """Test to see if setter works with real value."""
        converted = 10
        real = b"\x0A"

        bt = TLV(int_tag)
        assert not bt.value

        bt.value = real
        assert bt.value == converted
        assert bt._converted_value == converted
        assert bt._real_value == real

    def test_set_value_invalid_type(self, int_tag):
        """Test to see if setter raises an exception with invalid type"""
        bt = TLV(int_tag)
        assert not bt.value

        with pytest.raises(TypeError) as exc:
            bt.value = "invalid"
        assert "Invalid type str. Expected bytes or int" == str(exc.value)
