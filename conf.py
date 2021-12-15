from datetime import datetime
from os import getcwd
from pprint import pprint

DEBUG_MODE = True

BASE_PATH = getcwd() + '/'

with open(BASE_PATH + 'README.md') as readme_file:
    BASE_TITLE = readme_file.readline().strip() + " v" + datetime.today().strftime('%Y.%m.%d')
    for line in readme_file:
        pass
    COPYRIGHT = line

DESIGNER = "FirePython"

META_URL = '' # TBD

COUNTRY = 'all'

#pprint(dir())
