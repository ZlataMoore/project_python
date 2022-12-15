# -*- coding: utf-8 -*-
import dash_leaflet as dl
from dash import Dash, dcc, html, Input, Output, State
from flats_to_map import flats_to_map

app = Dash()
app.layout = html.Div([
    html.H1('Квартиры в Москве и МО'),
              dcc.RadioItems(
                id='pages',
                options=['1-100', '101-200', '201-300',
                         '301-500', '501-700', '701-800',
                         '801-1000', '1001-1200', '1201-1300'],
                value='1-100',
                inline=True
            ),
    html.Iframe(id='map', srcDoc=open('map.html', 'r', encoding='utf-8').read(), width='100%', height='600')
])
@app.callback(
    Output("map", "srcDoc"),
    Input("pages", "value"))
def display_choropleth(pages):
    flats_to_map(str(pages))

    fig = open('map.html', 'r', encoding='utf-8').read()

    return fig

if __name__ == '__main__':
    app.run_server()

