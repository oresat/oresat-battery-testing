import pytest
import battery_test_jig as BTJ

print(f"{BTJ.MEASURE_PINS[1]}") 

def test_measure_pin_2():
    assert BTJ.MEASURE_PINS[1] == 2, "Measure Pin 2 should equal 2."
        


