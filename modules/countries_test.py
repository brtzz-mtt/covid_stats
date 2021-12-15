from .countries import *

def test_countries():
    iso_mapping = Countries.get_mapping('iso', True)
    assert len(iso_mapping) == Countries.get_countries_amount()
    iso_mapping = Countries.get_mapping('test')
    assert next(iter(iso_mapping.values())) == None
