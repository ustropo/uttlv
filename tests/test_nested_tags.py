import pytest


class TestNestedTags:
    """Test various functionality with nested tag map configurations."""

    def test_nested_access(self, nested_tag):
        assert nested_tag["FIRST_NEST"]["SECOND_NEST"]["LEAF"] == 1

    def test_nested_parse(self, nested_tag, empty_nested_tag):
        """Tests that we can parse a nested structure from a byte array"""
        arr = nested_tag.to_byte_array()

        with pytest.raises(AttributeError):
            assert not empty_nested_tag.get("FIRST_NEST")

        empty_nested_tag.parse_array(arr)

        assert empty_nested_tag["FIRST_NEST"]["SECOND_NEST"]["LEAF"] == 1
