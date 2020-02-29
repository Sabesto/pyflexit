from pyflexit.common import Register, Regtype


def test_reg_count():
    register = Register(data_type="f", addr=1, regtype=Regtype.INPUT)
    assert register.count == 2

    register = Register(data_type="h", addr=1, regtype=Regtype.INPUT)
    assert register.count == 1

    register = Register(data_type="?", addr=1, regtype=Regtype.INPUT)
    assert register.count == 1
