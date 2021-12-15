from googletrans import LANGUAGES, Translator
from json import dump, load
from locale import LC_ALL, setlocale
from os import path

DEFAULT_LANGUAGE = 'en'

CACHE_FILE = path.dirname(__file__) + '/' + path.basename(__file__).split('.')[0] + '_cache.json'

class Polyglot:
    __cache = None
    __language = DEFAULT_LANGUAGE
    __translator = Translator()

    @staticmethod
    def get_european_languages(sort: bool = True) -> dict:
        european_languages = {
            'bg': 'български',
            'cs': 'čeština',
            'da': 'dansk',
            'de': 'deutsch',
            'el': 'eλληνικά',
            'en': 'english',
            'es': 'español',
            'et': 'eesti keel',
            'fi': 'suomalainen',
            'fr': 'français',
            'ga': 'gaeilge',
            'hr': 'hrvatski',
            'hu': 'magyar',
            'it': 'italiano',
            'lt': 'latvių',
            'lv': 'latviski',
            'mt': 'malti',
            'nl': 'nederlands',
            'pl': 'polskie',
            'pt': 'português',
            'ro': 'română',
            'sk': 'slovenský',
            'sl': 'slovenščina',
            'sv': 'svenska'
        }
        if sort:
            sorted_european_languages = {}
            for key, value in sorted(european_languages.items(), key = lambda item: item[1]):
                sorted_european_languages[key] = value
            return sorted_european_languages
        return european_languages

    @classmethod
    def __clear_cache(cls) -> None:
        cls.__cache = {}

    @classmethod
    def __save_cache(cls) -> None:
        with open(CACHE_FILE, 'w') as cache_file:
            dump(cls.__cache, cache_file,
                ensure_ascii = False,
                indent = 4,
                sort_keys = True
            )

    @staticmethod
    def get_languages() -> dict:
        return LANGUAGES

    @classmethod
    def get_language(cls) -> str:
        return cls.__language

    @classmethod
    def load_cache(cls) -> None:
        cls.__clear_cache()
        with open(CACHE_FILE) as cache_file:
            cls.__cache = load(cache_file)

    @classmethod
    def remove_translation(cls,
        text: str,
        target_language: str = None
    ) -> None:
        try:
            if target_language:
                del cls.__cache[text][target_language]
            else:
                del cls.__cache[text]
            cls.__save_cache()
        except KeyError:
            pass # TBD

    @classmethod
    def set_language(cls,
        language: str
    ) -> str:
        if language:
            cls.__language = language
        return cls.get_language()

    @classmethod
    def translate(cls,
        text: str,
        target_language: str = None
    ) -> str:
        destination_language = (cls.__language, target_language)[target_language != None]
        if destination_language == DEFAULT_LANGUAGE: return text
        if text not in cls.__cache: cls.__cache[text] = {}
        if destination_language not in cls.__cache[text]:
            try:
                translation = cls.__translator.translate(text,
                    src = DEFAULT_LANGUAGE,
                    dest = destination_language
                )
                if not translation._response or translation._response.status_code == 429: # too many requests..
                    return text
                else:
                    cls.__cache[text][destination_language] = translation.text
                    cls.__save_cache()
                    return translation.text
            except:
                return text
        else:
            return cls.__cache[text][destination_language] # cached translation

if not path.isfile(CACHE_FILE):
    with open(CACHE_FILE, 'w') as cache_file:
        dump({}, cache_file)
Polyglot.load_cache()

def gels(sort = True) -> dict:
    return Polyglot.get_european_languages(sort)

def gl() -> str:
    return Polyglot.get_language()

def gls() -> dict:
    return Polyglot.get_languages()

def rt(text: str, target_language: str = None) -> None:
    Polyglot.remove_translation(text, target_language)

def sl(language) -> str:
    return Polyglot.set_language(language)

def t(text: str, target_language: str = None) -> str:
    return Polyglot.translate(text, target_language)
