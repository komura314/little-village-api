# content of test_sample.py
def inc(x):
    return x + 1


def test_正常終了():
    assert inc(3) == 4


def test_異常終了():
    assert inc(3) == 5
