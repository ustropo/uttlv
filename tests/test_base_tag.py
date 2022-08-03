import unittest.mock as mock

import pytest

from uttlv.error import ValidationException
from uttlv.tag import BaseTag


class TestBaseTag:
    def test_create_abstract_exception(self):
        """Test to check if an attempt to create BaseTag should fail"""
        with pytest.raises(TypeError):
            BaseTag(10, "test", "string")

    def test_validate_disabled(self):
        """Test to check if validate method is called correctly when disabled."""
        with mock.patch.object(BaseTag, "__abstractmethods__", set()):
            bt = BaseTag(10, "test", "string")

            # It should returns true always
            assert not bt.should_validate
            assert bt.validate("string")

    def test_validate_enabled(self):
        """Test to check if validate method is called correctly."""
        with mock.patch.object(BaseTag, "__abstractmethods__", set()):
            bt = BaseTag(10, "test", "string", should_validate=True)

            assert bt.validate("string")

    def test_validate_fails(self):
        """Test to check if validate method fails and raises and exception."""
        with mock.patch.object(BaseTag, "__abstractmethods__", set()):
            # Mocks valid reason returns
            msg = "Invalid value"

            bt = BaseTag(10, "test", "string", should_validate=True)
            with mock.patch.object(bt, "_BaseTag__validate_value", return_value=msg):

                with pytest.raises(ValidationException) as exc:
                    assert not bt.validate("string")
                    assert str(exc) == msg

                bt.raise_if_invalid = False
                assert not bt.validate("string")

    def test_decode_length(self):
        """Test to check if decode length works."""
        with mock.patch.object(BaseTag, "__abstractmethods__", set()):
            bt = BaseTag(10, "test", "string")

            # Test with one length byte
            data = bytes([10])
            len_size, length = bt.decode_length(data)
            assert len_size == 1
            assert length == data[0]

            # Test with two length bytes
            data = bytes([0x81, 0x10])
            len_size, length = bt.decode_length(data)
            assert len_size == len(data)
            assert length == data[1]

            # Test with defined length size
            data = bytes([0x00, 0x10])
            bt.length_size = len(data)
            len_size, length = bt.decode_length(data)
            assert len_size == bt.length_size
            assert length == data[1]
