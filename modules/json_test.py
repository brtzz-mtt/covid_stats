from os import getcwd

from .json import *

def test_json():
    json = Json(getcwd() + '/modules/json_test.json')
    data = json.get_data()
    assert data['test'] == "data"
    date_now = Timestamp.get_today()
    data['date'] = date_now
    data = json.set_data(data)
    assert data['date'] == date_now
    json = json.save_data()
    assert json.get_data()['date'] == date_now
