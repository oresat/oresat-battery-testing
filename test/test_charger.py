import pytest
import sys
sys.path.insert(0, '..')
from battery_tester.libb6_interface_utils import battery_bank_from_pack_number


@pytest.mark.parametrize('packnum', range(4))
def test_battery_bank_from_pack_number(packnum):
	bank = battery_bank_from_pack_number(packnum)
	assert bank is not None
