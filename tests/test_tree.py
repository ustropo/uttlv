from uttlv import TLV


class TestTree:

    def test_tree_one(self, tag):
        """Test tree function."""
        tag[1] = 10
        tree = tag.tree()
        exp = '01: 10\r\n'

        assert exp == tree

    def test_tree_many(self, tag):
        """Test tree pretty function."""
        tag[1] = 10
        tag[2] = 20
        tag[3] = 'test'
        t1 = TLV()
        t1[1] = 10
        t1[2] = 30
        tag[7] = t1
        exp = '01: 10\r\n02: 20\r\n03: test\r\n07: \r\n    01: 10\r\n    02: 30\r\n\r\n'
        actual = tag.tree()

        assert exp == actual

    def test_tree_with_names(self, tag):
        tag[1] = 10
        tag[2] = 20
        tag[3] = 'test'
        t1 = TLV()
        t1[1] = 10
        t1[2] = 30
        tag[7] = t1
        exp = 'NUM_POINTS: 10\r\nIDLE_PERIOD: 20\r\nNAME: test\r\nRELATED: \r\n' \
              '    NUM_POINTS: 10\r\n    IDLE_PERIOD: 30\r\n\r\n'
        actual = tag.tree(use_names=True)

        assert exp == actual
