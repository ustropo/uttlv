from uttlv import *
import unittest

config = {
    0x01: {TLV.Config.Type: int, TLV.Config.Name: 'NUM_POINTS'},
    0x02: {TLV.Config.Type: int, TLV.Config.Name: 'IDLE_PERIOD'},
    0x03: {TLV.Config.Type: str, TLV.Config.Name: 'NAME'},
    0x04: {TLV.Config.Type: str, TLV.Config.Name: 'CITY'},
    0x05: {TLV.Config.Type: bytes, TLV.Config.Name: 'VERSION'},
    0x06: {TLV.Config.Type: bytes, TLV.Config.Name: 'DATA'},
    0x07: {TLV.Config.Type: TLV, TLV.Config.Name: 'RELATED'},
    0x08: {TLV.Config.Type: TLV, TLV.Config.Name: 'COMMENT'},
    0x09: {TLV.Config.Type: TLV, TLV.Config.Name: 'Empty'}
}


class TestParser(unittest.TestCase):
    '''Test array parser feature.'''

    @classmethod
    def setUpClass(cls):
        TLV.set_tag_map(config)

    def setUp(self):
        self.tlv = TLV(len_size=2)
        self.vtlv = TLV()

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
        t = TLV(len_size=2)
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
        t1 = TLV(len_size=2)
        t1[0x02] = 32
        t2 = TLV(len_size=2)
        t2[0x03] = 'teste'
        # Assert
        self.assertEqual(t1, self.tlv[0x07])
        self.assertEqual(t2, self.tlv[0x08])
        
        
    def test_auto_len_single_int(self):
        '''Test single int array parser.'''
        arr = [0x01, 0x04, 0x00, 0x00, 0x00, 0x10]
        self.vtlv.parse_array(arr)
        self.assertEqual(0x10, self.vtlv[0x01], 'Expected 16')

    def test_auto_len_single_str(self):
        '''Test single str array parser.'''
        arr = [0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.vtlv.parse_array(arr)
        self.assertEqual('teste', self.vtlv[0x03], 'Expected "teste"')

    def test_auto_len_single_bytes(self):
        '''Test single bytes array parser.'''
        arr = [0x05, 0x03, 0x01, 0x02, 0x03]
        self.vtlv.parse_array(arr)
        self.assertListEqual([1, 2, 3], list(self.vtlv[0x05]), 'Expected [1,2,3]')

    def test_auto_len_single_tlv(self):
        '''Test a single tlv tag'''
        t = TLV()
        t[0x01] = 25
        arr = [0x07, 0x07, 0x01, 0x04, 0x00, 0x00, 0x00, 0x19]
        self.vtlv.parse_array(arr)
        # Check values
        self.assertEqual(t, self.vtlv[0x07])

    def test_auto_len_nested_int(self):
        '''Test tlv object type'''
        arr = [0x01, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x04, 0x00, 0x00, 0x00, 0xFF]
        self.vtlv.parse_array(arr)
        self.assertEqual(10, self.vtlv[0x01])
        self.assertEqual(255, self.vtlv[0x02])

    def test_auto_len_nested_str(self):
        '''Test nested string object'''
        arr = [0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x04, 0x06, 0x6d, 0x61, 0x69, 0x73, 0x75, 0x6d]
        self.vtlv.parse_array(arr)
        # Check values
        self.assertEqual('teste', self.vtlv[0x03])
        self.assertEqual('maisum', self.vtlv[0x04])

    def test_auto_len_nested_byte(self):
        '''Test nested bytes object'''
        arr = [0x05, 0x03, 0x01, 0x02, 0x03, 0x06, 0x03, 0x05, 0x06, 0x07]
        self.vtlv.parse_array(arr)
        # Check values
        self.assertListEqual([1, 2, 3], list(self.vtlv[0x05]))
        self.assertListEqual([5, 6, 7], list(self.vtlv[0x06]))

    def test_auto_len_nested_tlv(self):
        '''Test a nested tlv tag'''
        arr = [0x07, 0x06, 0x02, 0x04, 0x00, 0x00, 0x00, 0x20, 0x08, 0x07, 0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.vtlv.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = 'teste'
        # Assert
        self.assertEqual(t1, self.vtlv[0x07])
        self.assertEqual(t2, self.vtlv[0x08])

    def test_auto_len_nested_tlv_with_empty(self):
        '''Test a nested tlv tag'''
        arr = [0x07, 0x06, 0x02, 0x04, 0x00, 0x00, 0x00, 0x20, 0x08, 0x07,
               0x03, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x09, 0x02, 0x01, 0x00]
        self.vtlv.parse_array(arr)
        # Check value
        t1 = TLV()
        t1[0x02] = 32
        t2 = TLV()
        t2[0x03] = 'teste'
        # Assert
        self.assertEqual(t1, self.vtlv[0x07])
        self.assertEqual(t2, self.vtlv[0x08])
        self.assertEqual(TLV(), self.vtlv[0x09])

    def test_auto_len_single_long_str(self):
        '''Test single str array parser.'''
        v = b'teste' * (2 ** 15 + 5)
        arr = b'\x03' + self.vtlv.encode_length(v) + v
        self.vtlv.parse_array(arr)
        self.assertEqual(v.decode('ascii'), self.vtlv[0x03], f'Expected "teste" repeating {2**15 + 5} times')
