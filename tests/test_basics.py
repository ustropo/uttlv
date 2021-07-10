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
    0x08: {TLV.Config.Type: TLV, TLV.Config.Name: 'COMMENT'}
}


class BasicTests(unittest.TestCase):
    """Class to execute some basic tests over package."""
    
    @classmethod
    def setUpClass(cls):
        TLV.set_tag_map(config)

    def setUp(self):
        self.tag = TLV(len_size=2)
        self.vtag = TLV()

    def test_int_one(self):
        """Test if a TLV object is corrected set to an array """
        self.tag[0x01] = 10
        # Create an array
        v = list(self.tag.to_byte_array())
        exp = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A]
        # Check value
        self.assertListEqual(exp, v, 'Value is not what expected.')

    def test_int_nested(self):
        """Test more than one int tag in an array."""
        self.tag[0x01] = 10
        self.tag[0x02] = 255
        # Create array 
        v = list(self.tag.to_byte_array())
        exp = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_str_one(self):
        """Test string tag"""
        self.tag[0x03] = 'teste'
        # Create array
        v = list(self.tag.to_byte_array())
        exp = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_str_nested(self):
        """Test string tag"""
        self.tag[0x03] = 'teste'
        self.tag[0x04] = 'maisum'
        # Create array
        v = list(self.tag.to_byte_array())
        exp = [0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65, 0x04, 0x00, 0x06, 0x6d, 0x61, 0x69, 0x73, 0x75, 0x6d]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_bytes_one(self):
        """Test array of bytes tag"""
        self.tag[0x05] = bytes([1, 2, 3])
        # Create array
        v = list(self.tag.to_byte_array())
        exp = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_bytes_nested(self):
        """Test array of bytes tag"""
        self.tag[0x05] = bytes([1, 2, 3])
        self.tag[0x06] = bytes([5, 6, 7])
        # Create array
        v = list(self.tag.to_byte_array())
        exp = [0x05, 0x00, 0x03, 0x01, 0x02, 0x03, 0x06, 0x00, 0x03, 0x05, 0x06, 0x07]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_tlv_one(self):
        """Test a TLV tag object"""
        t = TLV(len_size=2)
        t[0x01] = 25
        self.tag[0x07] = t
        # Create array
        v = list(self.tag.to_byte_array())
        exp = [0x07, 0x00, 0x07, 0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x19]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_tlv_nested(self):
        """Test multiple tlv tag object"""
        t1 = TLV(len_size=2)
        t1[0x02] = 32
        t2 = TLV(len_size=2)
        t2[0x03] = 'teste'
        self.tag[0x07] = t1
        self.tag[0x08] = t2
        # Create array
        v = list(self.tag.to_byte_array())
        exp = [0x07, 0x00, 0x07, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0x20, 0x08, 0x00, 0x08, 0x03, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_empty(self):
        """Test empty TLV object"""
        t = EmptyTLV(0x08, len_size=2)
        # Create array
        v = list(t.to_byte_array())
        exp = [0x08, 0x00, 0x00]
        # Check value
        self.assertListEqual(exp, v, 'Value not what expected')

    def test_key_name(self):
        '''Test access by key name.'''
        t = TLV()
        t['NUM_POINTS'] = 10

        self.assertEqual(t[1], 10)

    def test_attribute(self):
        '''Test access by attribute name.'''
        t = TLV()
        t['NUM_POINTS'] = 10

        self.assertEqual(t.NUM_POINTS, 10)

    def test_auto_len_single_byte(self):
        self.vtag[0x00] = b'1'
        expected = b'\x00\x01\x31'
        self.assertEqual(self.vtag.to_byte_array(), expected)

    def test_auto_len_double_byte(self):
        self.vtag[0x01] = bytes(c % 256 for c in range(2 ** 7 + 23))
        expected = b'\1\x81\x97' + self.vtag[0x01]
        self.assertEqual(self.vtag.to_byte_array(), expected)

    def test_auto_len_triple_byte(self):
        self.vtag[0x02] = bytes(c % 256 for c in range(2 ** 15 + 23))
        expected = b'\2\x82\x80\x17' + self.vtag[0x02]
        self.assertEqual(self.vtag.to_byte_array(), expected)

    def test_auto_len_multiple_sizes(self):
        self.vtag[0x00] = b'1'
        self.vtag[0x01] = bytes(c % 256 for c in range(2**7 + 23))
        self.vtag[0x02] = bytes(c % 256 for c in range(2**15 + 23))
        expected = (
                b'\0\1\x31\1\x81\x97' + self.vtag[0x01]
                + b'\2\x82\x80\x17' + self.vtag[0x02]
        )
        self.assertEqual(self.vtag.to_byte_array(), expected)
