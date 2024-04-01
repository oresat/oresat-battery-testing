import pytest
from libb6 import libb6

def test_device_bad_init():
    with pytest.raises(Exception):
        bad_desc = libb6.Device("bad")

def test_device_sys_info():
    sut = libb6.Device("good descriptor")
    info = sut.getSysInfo()
    assert info.this == that
