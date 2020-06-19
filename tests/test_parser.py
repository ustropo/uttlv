from uttlv import *
import unittest


config = {
    0x01: {'type': 'int', 'name': 'NUM_POINTS'},
    0x02: {'type': 'int', 'name': 'IDLE_PERIOD'},
    0x03: {'type': 'str', 'name': 'NAME'},
    0x04: {'type': 'str', 'name': 'CITY'},
    0x05: {'type': 'bytes', 'name': 'VERSION'},
    0x06: {'type': 'bytes', 'name': 'DATA'},
    0x07: {'type': 'TLV', 'name': 'RELATED'},
    0x08: {'type': 'TLV', 'name': 'COMMENT'}
}


class TestParser(unittest.TestCase):
    '''Test array parser feature.'''

    @classmethod
    def setUpClass(cls):
        TLV.set_tag_map(config)

    def setUp(self):
        self.tlv = TLV()

    def test_single_int(self):
        '''Test single int array parser.'''
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x10]
        self.tlv.parse_array(arr)
        self.assertEqual(0x10, self.tlv[0x01], 'Expected 16')

    def test_single_str(self):
        '''Test single str array parser.'''
        arr = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.tlv.parse_array(arr)
        self.assertEqual('teste', self.tlv[0x03], 'Expected "teste"')

    def test_single_bytes(self):
        '''Test single bytes array parser.'''
        arr = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03]
        self.tlv.parse_array(arr)
        self.assertListEqual([1, 2, 3], list(self.tlv[0x05]), 'Expected [1,2,3]')

    def test_single_tlv(self):
        '''Test a single tlv tag'''
        t = TLV()
        t[0x01] = 25
        arr = [0x07, 0x00, 0x07, 0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x19]
        self.tlv.parse_array(arr)
        # Check values
        self.assertEqual(t, self.tlv[0x07])

    def test_nested_int(self):
        '''Test tlv object type'''
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        self.tlv.parse_array(arr)
        self.assertEqual(10, self.tlv[0x01])
        self.assertEqual(255, self.tlv[0x02])

    def test_nested_str(self):
        '''Test nested string object'''
        arr = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x04, 0x00, 0x06, 0x6d, 0x61, 0x69, 0x73, 0x75, 0x6d]
        self.tlv.parse_array(arr)
        # Check values
        self.assertEqual('teste', self.tlv[0x03])
        self.assertEqual('maisum', self.tlv[0x04])

    def test_nested_byte(self):
        '''Test nested bytes object'''
        arr = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03, 0x06, 0x00, 0x03, 0x05, 0x06, 0x07]
        self.tlv.parse_array(arr)
        # Check values
        self.assertListEqual([1, 2, 3], list(self.tlv[0x05]))
        self.assertListEqual([5, 6, 7], list(self.tlv[0x06]))

    def test_nested_tlv(self):
        '''Test a nested tlv tag'''
        arr = [0x07, 0x00, 0x07, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0x20, 0x08, 0x00, 0x08, 0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.tlv.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = 'teste'
        # Assert
        self.assertEqual(t1, self.tlv[0x07])
        self.assertEqual(t2, self.tlv[0x08])
