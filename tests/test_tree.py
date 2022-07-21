import pytest

from uttlv import TLV


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


class TestTree:

    def setup_class(self):
        TLV.set_global_tag_map(config)

    def setup_method(self):
        self.tag = TLV()

    def test_tree_one(self):
        """Test tree function."""
        t = TLV()
        t[1] = 10
        tree = t.tree()
        exp = '01: 10\r\n'

        assert exp == tree

    def test_tree_many(self):
        """Test tree pretty function."""
        t = TLV()
        t[1] = 10
        t[2] = 20
        t[3] = 'test'
        t1 = TLV()
        t1[1] = 10
        t1[2] = 30
        t[7] = t1
        exp = '01: 10\r\n02: 20\r\n03: test\r\n07: \r\n    01: 10\r\n    02: 30\r\n\r\n'
        actual = t.tree()

        assert exp == actual

    def test_tree_with_names(self):
        t = TLV()
        t[1] = 10
        t[2] = 20
        t[3] = 'test'
        t1 = TLV()
        t1[1] = 10
        t1[2] = 30
        t[7] = t1
        exp = 'NUM_POINTS: 10\r\nIDLE_PERIOD: 20\r\nNAME: test\r\nRELATED: \r\n    NUM_POINTS: 10\r\n    IDLE_PERIOD: 30\r\n\r\n'
        actual = t.tree(use_names=True)

        assert exp == actual
