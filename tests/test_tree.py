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
        self.assertEqual(expected, t.tree())

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
        self.assertEqual(expected, t.tree(use_names=True))
