from main import *

def test_conf():
    assert isinstance(DEBUG_MODE, (bool, int))
    assert BASE_PATH
    assert isinstance(BASE_PATH, str)
    assert BASE_PATH == getcwd() + '/'

    with open(BASE_PATH + 'README.md') as readme_file:
        base_title = readme_file.readline().strip() + " v" + datetime.today().strftime('%Y.%m.%d')
        for line in readme_file:
            pass
        copyright = line

    assert BASE_TITLE
    assert isinstance(BASE_TITLE, str)
    assert base_title == BASE_TITLE
    assert COPYRIGHT
    assert isinstance(COPYRIGHT, str)
    assert copyright == COPYRIGHT

def test_main():
    assert app is not None
    assert str(type(app)) == "<class 'flask.app.Flask'>"
    assert app.static_folder == BASE_PATH + 'static'
    assert app.template_folder == 'templates'

    def test_route(app_view_function = 'index',
        title = BASE_TITLE,
        path = '/',
        status = '200 OK'
    ):
        assert app_view_function in app.view_functions
        with app.test_client().get(path) as response:
            assert response.charset == 'utf-8'
            assert response.mimetype == 'text/html'
            assert response.status == status
            if title:
                title = bytearray("<title>" + title + "</title>", 'utf-8')
                assert title in response.data
        with app.test_client().post(path) as response:
            assert response.charset == 'utf-8'
            assert response.mimetype == 'text/html'
            assert response.status == '405 METHOD NOT ALLOWED'

    test_route()
    test_route('index_p0',
        title = False,
        path = '/<p0>/',
        status = '404 NOT FOUND'
    )
    test_route('index_p0',
        title = BASE_TITLE + " | english",
        path = '/en/',
        status = '200 OK'
    )
    test_route('index_p0',
        title = BASE_TITLE + " | License",
        path = '/license/',
        status = '200 OK'
    )
    test_route('index_p0',
        title = BASE_TITLE + " | Readme",
        path = '/readme/',
        status = '200 OK'
    )
    test_route('index_p0_p1',
        title = False,
        path = '/<p0>/<p1>/',
        status = '404 NOT FOUND'
    )
    test_route('index_p0_p1',
        title = BASE_TITLE + " | all countries",
        path = '/en/all/',
        status = '200 OK'
    )
    test_route('index_p0_p1',
        title = BASE_TITLE + " | United Kingdom",
        path = '/en/gbr/',
        status = '200 OK'
    )
    test_route('index_p0_p1',
        title = BASE_TITLE + " | english",
        path = '/en/test/',
        status = '200 OK'
    )

from modules.csv_test import *; test_csv()
from modules.json_test import *; test_json()
from modules.polyglot_test import *; test_polyglot()
from modules.timestamp_test import *; test_timestamp()
