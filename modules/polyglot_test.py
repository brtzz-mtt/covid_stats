from .polyglot import *

from random import choice

def test_polyglot():
    assert len(gels(False)) == 24
    assert gels() == {
        'da': 'dansk',
        'de': 'deutsch',
        'et': 'eesti keel',
        'en': 'english',
        'es': 'español',
        'el': 'eλληνικά',
        'fr': 'français',
        'ga': 'gaeilge',
        'hr': 'hrvatski',
        'it': 'italiano',
        'lv': 'latviski',
        'lt': 'latvių',
        'hu': 'magyar',
        'mt': 'malti',
        'nl': 'nederlands',
        'pl': 'polskie',
        'pt': 'português',
        'ro': 'română',
        'sk': 'slovenský',
        'sl': 'slovenščina',
        'fi': 'suomalainen',
        'sv': 'svenska',
        'cs': 'čeština',
        'bg': 'български'
    }
    assert gl() == DEFAULT_LANGUAGE
    assert gls() == LANGUAGES
    assert sl(DEFAULT_LANGUAGE) == DEFAULT_LANGUAGE
    assert t('dummy') == 'dummy'
    rt('Hello World!', choice(list(gels())))
    for language in gels():
        translation = t('Hello World!', language)
        assert translation != 'Hello World!' \
            or (translation == 'Hello World!' and language == DEFAULT_LANGUAGE)
