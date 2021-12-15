from conf import *

from flask import abort, Flask, render_template
from jinja2 import TemplateNotFound
from markdown import markdown
from os import path

from modules.countries import *
from modules.csv import *
from modules.json import *
from modules.polyglot import *
from modules.timestamp import *

from data import generate_plots

country_names = {**{'all': t("all countries")}, **gm('name')}

def flask_template_render(template: str = 'index.html',
    title: str = BASE_TITLE,
    **kwargs
) -> str:
    if COUNTRY != 'all':
        generate_plots(COUNTRY)
    return render_template(template,
        title = title,
        meta = {
            'copyright': COPYRIGHT,
            'description': '', # TBD
            'designer': DESIGNER,
            'keywords': '', #TBD
            'url': META_URL
        },
        data = {**kwargs, **{
            'country_data': gcd(COUNTRY),
            'country_isos': gm('iso'),
            'country_names': country_names,
            'current_country': COUNTRY,
            'data_links': Json(BASE_PATH + 'data/links.json').get_data()
        }},
        available_languages = gels(),
        current_language = gl(),
        t = t
    )

app = Flask(__name__)

@app.route('/')
def index(title: str = BASE_TITLE):
    return flask_template_render(title = title)

@app.route('/<p0>/')
def index_p0(p0, title: str = BASE_TITLE):
    if p0 in gels():
        sl(p0)
        global COUNTRY
        COUNTRY = 'all'
        return index(BASE_TITLE + " | " + gels()[gl()])
    file = p0.upper()
    md_file = p0.upper() + '.md'
    if path.exists(file):
        with open(file) as file:
            return flask_template_render('pages/index.html',
                title = BASE_TITLE + " | " + p0.capitalize(),
                article = file.read().replace("\n\n", "<br /><br />")
            )
    elif path.exists(md_file):
        with open(md_file ) as file:
            return flask_template_render('pages/index.html',
                title = BASE_TITLE + " | " + p0.capitalize(),
                article = markdown(file.read())
            )
    else:
        try:
            return flask_template_render('pages/' + p0 + '.html',
                title = title
            )
        except TemplateNotFound:
            abort(404)

@app.route('/<p0>/<p1>/')
def index_p0_p1(p0, p1, title = None):
    if p0 in gels():
        sl(p0)
    else:
        abort(404)
    if p1 in country_names:
        global COUNTRY
        COUNTRY = p1
        return index(BASE_TITLE + " | " + t(country_names[COUNTRY]))
    else:
        return index_p0(p0, title)

if __name__ == '__main__':
    app.run(debug = DEBUG_MODE)
    pprint(vars(app))
