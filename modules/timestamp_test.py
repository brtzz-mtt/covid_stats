from .timestamp import *

def test_timestamp():
    assert gn() == datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    assert gt() == datetime.now().strftime('%Y-%m-%d')
    timestamp = Timestamp()
    assert timestamp.get_date() == datetime.fromtimestamp(time()).strftime('%Y-%m-%d')
    assert timestamp.get_timestamp() == datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
