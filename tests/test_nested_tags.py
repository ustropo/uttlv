import pytest

from uttlv import TLV

config = {
    0x01: {TLV.Config.Name: 'FIRST_NEST', TLV.Config.Type: {
        0x01: {TLV.Config.Name: 'SECOND_NEST', TLV.Config.Type: {
            0x01: {TLV.Config.Name: 'LEAF', TLV.Config.Type: int}
        }}
    }},

    0x02: {TLV.Config.Type: int, TLV.Config.Name: 'NON_NESTED_DATA'}
}


class TestNestedTags:
    """Test various functionality with nested tag map configurations."""

    def setup_class(self):
        self.t = TLV()
        self.t[0x01] = TLV()
        self.t[0x01][0x01] = TLV()
        self.t[0x01][0x01][0x01] = 1
        self.t[0x02] = 42

    def test_nested_access(self):
        self.t.set_local_tag_map(config)

        assert self.t['FIRST_NEST']['SECOND_NEST']['LEAF'] == 1

    def test_nested_parse(self):
        """Tests that we can parse a nested structure from a byte array"""
        arr = self.t.to_byte_array()
        t = TLV()
        t.set_local_tag_map(config)
        t.parse_array(arr)

        assert t['FIRST_NEST']['SECOND_NEST']['LEAF'] == 1
