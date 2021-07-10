from uttlv import *
import unittest

from uttlv.tlv import TLVIterator

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


class TestIterate(unittest.TestCase):
    '''Test iteration trough top-level tags.'''

    @classmethod
    def setUpClass(cls):
        TLV.set_tag_map(config)


    def setUp(self):
        self.tlv = TLV(len_size=2)
        self.vtlv = TLV()
        '''Int array.'''
        arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x10]
        self.tlv.parse_array(arr)

        '''str array'''
        arr = [0x02, 0x00, 0x05, 0x74, 0x65, 0x73, 0x74, 0x65]
        self.tlv.parse_array(arr)

        '''tlv object type'''
        arr = [0x08, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
        self.tlv.parse_array(arr)

    def test_iterator_available(self):
        '''Test if correct iterator available'''
        it = iter(self.tlv)

        self.assertIsInstance(it, TLVIterator, 'Expected TLVIterator instance')

    def test_iteration_trough_objects(self):
        '''Test iteration trough parsed values'''
        it = iter(self.tlv)

        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 8)

    def test_iteration_raise_exception(self):
        '''Test out of index iteration '''
        it = iter(self.tlv)

        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 8)
        self.assertRaises(StopIteration, next, it)

    def test_iteration_empty_raise_exception(self):
        '''Test empty class'''
        tlv = TLV(len_size=2)
        it = iter(tlv)

        self.assertRaises(StopIteration, next, it)