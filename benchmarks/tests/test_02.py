def run(mod):
    assert mod.add_item("a") == ["a"]
    assert mod.add_item("b") == ["b"]
    assert mod.add_item("c", ["x"]) == ["x", "c"]
