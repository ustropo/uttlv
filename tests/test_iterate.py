import pytest

from uttlv.tlv import TLVIterator


class TestIterator:
    """Test iteration trough top-level tags."""

    def test_iterator_available(self, multi_tag):
        """Test if correct iterator available"""
        it = iter(multi_tag)

        assert isinstance(it, TLVIterator)

    def test_iteration_trough_objects(self, multi_tag):
        """Test iteration trough parsed values"""
        it = iter(multi_tag)

        assert next(it) == 1
        assert next(it) == 2
        assert next(it) == 8

    def test_iteration_raise_exception(self, multi_tag):
        """Test out of index iteration"""
        it = iter(multi_tag)

        assert next(it) == 1
        assert next(it) == 2
        assert next(it) == 8

        with pytest.raises(StopIteration):
            next(it)

    def test_iteration_empty_raise_exception(self, tag):
        """Test empty class"""
        it = iter(tag)

        with pytest.raises(StopIteration):
            next(it)
