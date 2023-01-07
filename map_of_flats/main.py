# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, Input, Output
from flats_to_map import flats_to_map
import dash_bootstrap_components as dbc

from project_python.banki_parser.start_scrapper import get_banks


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

ALLOWED_CHOICE = (
    "initialFee",
    "salary(default: 30 000)", "If You have child born after 2018, enter 1, else 0(default: 1)"
)
button = html.Div(
    [
        dcc.Markdown('''Введите значение: Первоначальный взнос(стандартно: 2 000 000), 
    Максимальная ежемесячная плата по ипотеке(стандартно: 30 000), Если у вас есть ребенок, рожденный до 2018 года?, введите 1, иначе 0(стандартно: 1)'''),
        dcc.Input(id="fee", type="number", placeholder="Первоначальный взнос"),
        dcc.Input(
            id="max_payment", type="number", placeholder="Максимальная ежемесячная плата по ипотеке",
        ),
dcc.Input(
            id="child", type="number", placeholder="Есть ли у вас ребенок, рожденный до 2018 года?",
        ),
        html.Hr(),
        html.Div(id="number-out"),
    ],
    style={'text-align': 'center'}
)


app.layout = html.Div([
    html.H1('Квартиры в Москве и МО'),
    html.Div(
        dcc.RadioItems(
            id='pages',
            options=['old 1-100', 'old 101-200', 'old 201-300',
                     'old 301-500', 'old 501-700', 'old 701-800',
                     'old 801-1000', 'old 1001-1200', 'old 1201-1300',
                     'new 1-100', 'new 101-200', 'new 201-300', 'new 301-400',
                     'new 401-500'],
            value='old 1-100',
            inline=True,
            style={'padding': '5px', 'background-color': '#cdcdcd', 'margin': '3px'}
        ),
        style={'width': '90%'}
    ),
    button,
    html.Iframe(id='map', srcDoc=open('map.html', 'r', encoding='utf-8').read(), width='100%', height='600')
],
style={'text-align': 'center'})

PAYLOAD = {
    'fee': 2_000_000,
    'max_payment': 30_000,
    'child': 1,
    'type': 'new'
}

@app.callback(
    Output("number-out", "children"),
    Input("fee", "value"),
    Input("max_payment", "value"),
    Input("child", "value")
)
def number_render(fee, max_payment, child):
    if fee is not None and int(fee) >= 0:
        PAYLOAD['fee'] = int(fee)
    else:
        fee = str(PAYLOAD['fee'])
    if fee is not None and int(fee) >= 0:
        PAYLOAD['max_payment'] = int(max_payment)
    else:
        max_payment = str(PAYLOAD['max_payment'])
    if child == '0' or child == '1':
        PAYLOAD['child'] = int(child)
    else:
        child = str(PAYLOAD['child'])
    return "Первоначальный взнос: {}, Максимальная ежемесячная плата по ипотеке:" \
           " {}, Есть ли у вас ребенок, рожденный до 2018 года?: {}" \
           "".format(fee, max_payment, 'Да' if int(child) else 'Нет')


@app.callback(
    Output("map", "srcDoc"),
    Input("pages", "value"))
def display_choropleth(pages):
    flats_to_map(str(pages), [1, 1, 1])
    PAYLOAD['type'] = pages[:3]

    fig = open('map.html', 'r', encoding='utf-8').read()

    return fig


@server.route('/mortgage/<int:price>')
def mortgage(price):
    return get_banks(price, PAYLOAD['fee'], PAYLOAD['child'], PAYLOAD['type'], PAYLOAD['max_payment'])


if __name__ == '__main__':
    app.run_server()
