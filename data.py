from conf import *

from meteostat import Daily, Point
from pandas import DataFrame, date_range, options, read_csv, to_datetime
from plotly import graph_objects

from modules.countries import *
from modules.csv import *
from modules.polyglot import *
from modules.timestamp import *

options.plotting.backend = "plotly"

today = Timestamp.get_today()

COUNTRY_CSV_PATH = BASE_PATH + 'data/covid_countries_' + today + '.csv'
DATA_CSV_PATH = BASE_PATH + 'data/data.csv'#_' + today + '.csv'

data_covid_countries_today = Csv(COUNTRY_CSV_PATH,
    url = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv'
).get_data()

def process_data_covid_countries_today(existing_data = None):
    index = []
    if not existing_data:
        data = [[
            'date',
            'datum',
            'country',
            'country_filter',
            'confirmed',
            'confirmed_increment',
            'recovered',
            'recovered_increment',
            'deaths',
            'deaths_increment',
            'tavg',
            'tmin',
            'tmax'
        ]]
    else:
        for i in range(1, len(existing_data)):
            index.append(existing_data[i][0] + "_" + existing_data[i][3])
        data = existing_data
    #print(index)
    #return
    available_countries = gm('name', True)
    current_country, country_filter = None, None
    confirmed_before, recovered_before, deaths_before = 0, 0, 0
    data_length = len(data_covid_countries_today)
    current_status = None
    for i in range(1, data_length):
        #print(chr(27) + "[2J" + "Preprocessing: " + "{:.2f}".format((i / data_length) * 100) + "%..")
        status = "{:.1f}".format((i / data_length) * 100) + "%.."
        if status != current_status:
            print("Preprocessing: " + status)
            current_status = status
        country = data_covid_countries_today[i][1].replace("*", '')
        if country == 'Burma':
            country = "Myanmar"
        elif country == 'Czechia':
            country = 'Czech Republic'
        elif country == 'Holy See':
            country = 'Vatican City'
        elif country == 'Togo':
            country = 'Togolese Republic'
        elif country == 'Turkey':
            country = 'Republic of Turkey'
        elif country == 'US':
            country = 'USA'
        if country not in available_countries:
            continue # TBD
        elif country != current_country:
            current_country = country
            country_filter = available_countries[country]
            confirmed_before, recovered_before, deaths_before = 0, 0, 0
            if not existing_data:
                data.append(['2020-01-01', '2020-01-01', country, country_filter, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            country_data = gcd(available_countries[country])
            point = Point(country_data['coordinates']['latitude'], country_data['coordinates']['longitude'], 0)
            point.radius = 1000000
        confirmed = int(data_covid_countries_today[i][2])
        recovered = int(data_covid_countries_today[i][3])
        deaths = int(data_covid_countries_today[i][4])
        confirmed_increment = confirmed - confirmed_before
        recovered_increment = recovered - recovered_before
        deaths_increment = deaths - deaths_before
        confirmed_before, recovered_before, deaths_before = confirmed, recovered, deaths
        
        # checks if line already present and valid, and if not generates it..
        if data_covid_countries_today[i][0] + "_" + country_filter in index:
            continue

        try: # because this call generates a bottleneck..
            daily = Daily(point, datetime.strptime(data_covid_countries_today[i][0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime(data_covid_countries_today[i][0] + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
            daily_data = daily.fetch().iloc[0]
            tavg = daily_data['tavg']
            tmin = daily_data['tmin']
            tmax = daily_data['tmax']
        except:
            tavg = 0
            tmin = 0
            tmax = 0
        data.append([
            data_covid_countries_today[i][0],
            data_covid_countries_today[i][0],
            country,
            country_filter,
            confirmed,
            confirmed_increment,
            recovered,
            recovered_increment,
            deaths,
            deaths_increment,
            tavg,
            tmin,
            tmax
        ])
        index.append(country_filter + data_covid_countries_today[i][0])
    return data

def get_data_frame():
    data = Csv(DATA_CSV_PATH).get_data()
    if not Csv.exists(DATA_CSV_PATH) or True:
        Csv(DATA_CSV_PATH,
            data = process_data_covid_countries_today(data)
        )
    data = read_csv(DATA_CSV_PATH)
    data.index = to_datetime(data['date'], format = '%Y-%m-%d')
    data['datum'] = to_datetime(data['datum'], format = '%Y-%m-%d')
    return data

data = get_data_frame()

def generate_plots(country):
    labels = {
        'confirmed_increment': "positives",
        'deaths_increment': "deaths"
    }
    country_data = data.loc[(data['country_filter'] == country)]
    max = country_data.confirmed_increment.max()#; print(max)
    max_tavg = country_data.tavg.max()
    min_tavg = country_data.tavg.min()
    for year in ['2020', '2021', 'projection_2022', '2022']:
        plot_path = BASE_PATH + 'templates/plots/' + country + '_' + year + '.html'
        if path.exists(plot_path):
            continue
        if 'projection_' in year:
            data_frame = country_data.groupby([country_data.index.month, country_data.index.day]).mean()
            year = year[-4:]
            start_date = year + '-01-01'
            end_date = year + '-12-31'
            data_range = date_range(start = start_date, end = end_date)
            try:
                data_frame['datum'] = data_range#data_frame.assign(datum = data_range)
            except ValueError:
                data_frame.drop((2, 29), axis=0, inplace=True)
                data_frame['datum'] = data_range
        else:
            start_date = year + '-01-01'
            end_date = year + '-12-31'
            data_frame = country_data.loc[(country_data['datum'] >= start_date) & (country_data['datum'] <= end_date)]
            data_range = date_range(start = start_date, end = end_date)
            data_frame.reindex(data_range, fill_value = 0)
        figure = data_frame.plot.area( # see https://plotly.com/python-api-reference/generated/plotly.express.area.html
            x = 'datum',
            y = ['confirmed_increment', 'deaths_increment'],
            labels = {
                'datum': '',
                'value': '',
                'variable': ''
            }
        )
        figure.for_each_trace(lambda t: t.update(
            name = labels[t.name],
            legendgroup = labels[t.name],
            hovertemplate = t.hovertemplate.replace(t.name, labels[t.name])
        ))
        figure.add_trace(graph_objects.Scatter(
            x = data_frame.datum,
            y = data_frame.tavg,
            name = "avg. temp. °C",
            yaxis = 'y2'
        ))
        figure.update_xaxes(
            dtick = 'M1',
            tickformat = '%B'
        )
        figure.update_yaxes(
            range = [0, max * 1.05]
        )
        figure.update_layout(
            margin = {
                't': 25,
                'r': 0,
                'b': 0,
                'l': 0,
                'pad': 0
            },
            paper_bgcolor = 'rgba(0,0,0,0)',
            yaxis2 = {
                'overlaying': 'y',
                'range': [min_tavg, max_tavg * 1.05],
                'side': 'right'
            }
        )
        figure.write_html(plot_path, # see https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_html.html
            full_html = False,
            include_plotlyjs = 'cdn'
        )
