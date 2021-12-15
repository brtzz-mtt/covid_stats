from os import getcwd, remove

from .csv import *

def test_csv():
    csv = Csv(getcwd() + '/modules/csv_test.csv')
    assert len(csv.get_data()) == 5
    assert csv.get_headers() == ['dummy_header_0', 'dummy_header_1', 'dummy_header_2', 'dummy_header_3']
    data_raw = csv.get_data_raw()
    assert type(data_raw) == str
    data = csv.get_data()
    assert type(data) == list
    file_path = getcwd() + '/modules/csv_test_data.csv'
    csv = Csv(file_path, 'https://gist.githubusercontent.com/rnirmal/f3afd35401d788e5256bea03c72b4954/raw/4b7967fb1b7cc6932a39d25f6657a496d569cca9/datasources.csv')
    csv = Csv(file_path, None, data)
    assert csv.get_data() == data
    remove(file_path)
