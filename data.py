from conf import *

from meteostat import Daily, Point
from pandas import date_range, options, read_csv, to_datetime
from plotly import graph_objects

from modules.countries import *
from modules.csv import *
from modules.polyglot import *
from modules.timestamp import *

options.plotting.backend = "plotly"

today = Timestamp.get_today()

data_covid_countries_today = Csv(BASE_PATH + 'data/covid_countries_' + today + '.csv',
    url = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv'
).get_data()

def process_data_covid_countries_today():
    data = [[
        'date',
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
    available_countries = gm('name', True)
    current_country, country_filter = None, None
    confirmed_before, recovered_before, deaths_before = 0, 0, 0
    data_length = len(data_covid_countries_today)
    for i in range(1, data_length):
        print(chr(27) + "[2J" + "Preprocessing: " + "{:.2f}".format((i / data_length) * 100) + "%..")
        country = data_covid_countries_today[i][1].replace("*", '')
        if country not in available_countries:
            continue # TBD
        elif country == 'Burma':
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
        elif country != current_country:
            current_country = country
            country_filter = available_countries[country]
            confirmed_before, recovered_before, deaths_before = 0, 0, 0
            data.append(['2020-01-01', country, country_filter, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            country_data = gcd(available_countries[country])
            point = Point(country_data['coordinates']['latitude'], country_data['coordinates']['longitude'], 0)
            point.radius = 1000000
        confirmed = int(data_covid_countries_today[i][2])
        recovered = int(data_covid_countries_today[i][3])
        deaths = int(data_covid_countries_today[i][4])
        confirmed_increment = confirmed - confirmed_before
        recovered_increment = recovered - recovered_before
        deaths_increment = deaths - deaths_before
        daily = Daily(point, datetime.strptime(data_covid_countries_today[i][0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime(data_covid_countries_today[i][0] + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
        try:
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
        confirmed_before, recovered_before, deaths_before = confirmed, recovered, deaths
    return data

def get_data_frame():
    data_csv_path = BASE_PATH + 'data/data_' + today + '.csv'
    if not Csv.exists(data_csv_path):
        Csv(data_csv_path,
            data = process_data_covid_countries_today()
        )
    data = read_csv(data_csv_path)
    data['date'] = to_datetime(data['date'], format = '%Y-%m-%d')
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
    for year in ['2020', '2021']:
        plot_path = BASE_PATH + 'templates/plots/' + country + '_' + year + '.html'
        if path.exists(plot_path):
            continue
        start_date = year + '-01-01'
        end_date = year + '-12-31'
        data_frame = country_data.loc[(country_data['date'] >= start_date) & (country_data['date'] <= end_date)]
        data_range = date_range(start = start_date, end = end_date)
        data_frame.reindex(data_range, fill_value = 0)
        figure = data_frame.plot.area( # see https://plotly.com/python-api-reference/generated/plotly.express.area.html
            x = 'date',
            y = ['confirmed_increment', 'deaths_increment'],
            labels = {
                'date': '',
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
            x = data_frame.date,
            y = data_frame.tavg,
            name = "avg. °C",
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
