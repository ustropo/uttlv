from tkinter import W
from uttlv import *
import unittest

config = {
    0x01: {TLV.Config.Name: 'FIRST_NEST', TLV.Config.Type: {
        0x01: {TLV.Config.Name: 'SECOND_NEST', TLV.Config.Type: {
            0x01: {TLV.Config.Name: 'LEAF', TLV.Config.Type: int}
        }}
    }},

    0x02: {TLV.Config.Type: int, TLV.Config.Name: 'NON_NESTED_DATA'}
}



class TestNestedTags(unittest.TestCase):
    '''Test various functionality with nested tag map configurations.'''

    def create_tlv(self) -> TLV:
        '''Manually create structure equivalent to config.'''
        t = TLV()
        t[0x01] = TLV()
        t[0x01][0x01] = TLV()
        t[0x01][0x01][0x01] = 1
        t[0x02] = 42
        return t

    def test_nested_access(self):
        t = self.create_tlv()
        t.set_local_tag_map(config)

        self.assertEqual(t['FIRST_NEST']['SECOND_NEST']['LEAF'], 1)

    def test_nested_parse(self):
        '''Tests that we can parse a nested structure from a byte array'''
        arr = self.create_tlv().to_byte_array()
        t = TLV()
        t.set_local_tag_map(config)
        t.parse_array(arr)

        t['FIRST_NEST']
        t['FIRST_NEST']['SECOND_NEST']
        self.assertEqual(t['FIRST_NEST']['SECOND_NEST']['LEAF'], 1)

    def check_if_value_exists(self, obj, value):
        try:
            obj[value]
            self.fail("Extra non-TLV value was created")
        # KeyError is the final error generated if we have a tag map defined but the object isn't there
        except KeyError:
            pass

    def test_only_nested_tlvs_created(self):
        t = TLV()
        t.set_local_tag_map(config)

        self.check_if_value_exists(t, 'NON_NESTED_DATA')
        self.check_if_value_exists(t['FIRST_NEST']['SECOND_NEST'], 'LEAF')
