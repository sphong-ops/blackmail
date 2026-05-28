def run(mod):
    assert mod.reverse_list([1, 2, 3]) == [3, 2, 1]
    assert mod.reverse_list([]) == []
    assert mod.reverse_list(["a"]) == ["a"]
