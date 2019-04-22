
import clrtools



def test_is_string():
    s = clrtools.joke()
    assert isinstance(s, str)