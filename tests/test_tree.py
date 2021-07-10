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


class TreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TLV.set_tag_map(config)

    def setUp(self):
        self.tag = TLV()

    def test_tree_one(self):
        '''Test tree function.'''
        t = TLV()
        t[1] = 10
        tree = t.tree()
        expected = '01: 10\r\n'
        self.assertEqual(expected, tree)

    def test_tree_many(self):
        '''Test tree pretty function.'''
        t = TLV()
        t[1] = 10
        t[2] = 20
        t[3] = 'test'
        t1 = TLV()
        t1[1] = 10
        t1[2] = 30
        t[7] = t1
        expected = '01: 10\r\n02: 20\r\n03: test\r\n07: \r\n    01: 10\r\n    02: 30\r\n\r\n'
        actual = t.tree()
        self.assertEqual(expected, actual)

    def test_tree_with_names(self):
        t = TLV()
        t[1] = 10
        t[2] = 20
        t[3] = 'test'
        t1 = TLV()
        t1[1] = 10
        t1[2] = 30
        t[7] = t1
        expected = 'NUM_POINTS: 10\r\nIDLE_PERIOD: 20\r\nNAME: test\r\nRELATED: \r\n    NUM_POINTS: 10\r\n    IDLE_PERIOD: 30\r\n\r\n'
        actual = t.tree(use_names=True)
        self.assertEqual(expected, actual)
