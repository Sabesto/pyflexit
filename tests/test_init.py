import pytest

import pyflexit


def test_init():
    unit = pyflexit.aggregate("dummy", 21, model="CI66")
    assert isinstance(unit, pyflexit.CI66)

    unit = pyflexit.aggregate("dummy", 1, model="Nordic")
    assert isinstance(unit, pyflexit.Nordic)

    with pytest.raises(ValueError):
        pyflexit.aggregate("dummy", 1, model="Illegal")
