def run(mod):
    assert mod.count_vowels("hello universe") == 6
    assert mod.count_vowels("aeiou") == 5
    assert mod.count_vowels("xyz") == 0
    assert mod.count_vowels("Quick Brown Fox") == 4
