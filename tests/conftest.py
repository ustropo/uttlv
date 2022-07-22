import pytest

from uttlv import TLV

global_tag_map = {
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

nested_tag_map = {
    0x01: {TLV.Config.Name: 'FIRST_NEST', TLV.Config.Type: {
        0x01: {TLV.Config.Name: 'SECOND_NEST', TLV.Config.Type: {
            0x01: {TLV.Config.Name: 'LEAF', TLV.Config.Type: int}
        }}
    }},

    0x02: {TLV.Config.Type: int, TLV.Config.Name: 'NON_NESTED_DATA'}
}


@pytest.fixture(scope="session")
def apply_global_map():
    TLV.set_global_tag_map(global_tag_map)


@pytest.fixture(scope="function")
def tag(apply_global_map):
    yield TLV(len_size=2)


@pytest.fixture(scope="function")
def auto_len_tag(apply_global_map):
    yield TLV()


@pytest.fixture(scope="function")
def multi_tag(tag):
    # int object type
    arr = [0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0xA9]
    tag.parse_array(arr)

    # str object type
    arr = [0x02, 0x00, 0x04, 0x30, 0x31, 0x32, 0x33]
    tag.parse_array(arr)

    # tlv object type
    arr = [0x08, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF]
    tag.parse_array(arr)

    yield tag


@pytest.fixture(scope="function")
def empty_nested_tag():
    tag = TLV()
    tag.set_local_tag_map(nested_tag_map)
    yield tag


@pytest.fixture(scope="function")
def nested_tag(empty_nested_tag):
    tag = TLV()
    tag[0x01] = TLV()
    tag[0x01][0x01] = TLV()
    tag[0x01][0x01][0x01] = 1
    tag[0x02] = 42
    tag.set_local_tag_map(nested_tag_map)

    yield tag
