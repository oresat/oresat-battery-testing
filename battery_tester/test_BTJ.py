import pytest
import battery_test_jig as BTJ

#Tests for global variables:
@pytest.mark.parametrize("index, expected", [(0,0), (1,2), (2,4), (3,6)])
def test_measure_pins(index, expected):
    assert BTJ.MEASURE_PINS[index] == expected, "Check MEASURE_PINS in battery_test_jig.py"

@pytest.mark.parametrize("index, expected", [(0,8), (1,9), (2,10), (3,11)])
def test_temperature_pins(index, expected):
    assert BTJ.TEMPERATURE_PINS[index] == expected, "Check TEMPERATURE_PINS in battery_test_jig.py"

@pytest.mark.parametrize("index, expected", [(0,18), (1,17), (2,16), (3,15)])
def test_voltage_neg_pins(index, expected):
    assert BTJ.VOLTAGE_NEG_PINS[index] == expected, "Check VOLTAGE_NEG_PINS in battery_test_jig.py"

@pytest.mark.parametrize("index, expected", [(0,7), (1,5), (2,3), (3,1)])
def test_charge_bank_pins(index, expected):
    assert BTJ.CHARGE_BANK_PINS[index] == expected, "Check CHARGE_BANK_PINS in battery_test_jig.py"

@pytest.mark.parametrize("index, expected", [(0,37), (1,36), (2,35), (3,34)])
def test_voltage_pos_pins(index, expected):
    assert BTJ.VOLTAGE_POS_PINS[index] == expected, "Check VOLTAGE_POS_PINS in battery_test_jig.py"

@pytest.mark.parametrize("index, expected", [(0,1.2)])
def test_charger_serial_nums(index, expected):
    assert BTJ.CHARGERS[index] == expected, "Check CHARGERS in battery_test_jig.py"
