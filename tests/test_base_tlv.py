import unittest.mock as mock

import pytest

from uttlv.tlv import BaseTLV


class TestBaseTag:
    def test_create_abstract_exception(self):
        """Test to check if an attempt to create BaseTLV should fail"""
        with pytest.raises(TypeError):
            BaseTLV(None)

    def test_get_value(self):
        """Test if method value property is working."""
        with mock.patch.object(BaseTLV, "__abstractmethods__", set()):
            converted = 10
            real = b"\x0A"
            # TODO: change this to unknown tag
            bt = BaseTLV(None, _real_value=real)

            # It should return real value
            assert bt.value == real

            # It should return converted value
            bt = BaseTLV(None, _real_value=real, _converted_value=converted)
            assert bt.value == converted

    def test_set_value(self):
        """Test to see if setter for value is working."""
        converted = 10
        real = b"\x0A"

        with mock.patch.object(BaseTLV, "__abstractmethods__", set()):
            bt = BaseTLV(None)

            with mock.patch.object(bt, "_convert_value", return_value=(real, converted)):
                assert not bt.value
                bt.value = converted
                assert bt.value == converted
                assert bt._converted_value == converted
                assert bt._real_value == real
