def run(mod):
    assert mod.average(3, 4) == 3.5
    assert mod.average(10, 20) == 15.0
    assert mod.average(0, 0) == 0.0
    assert mod.average(7, 8) == 7.5
