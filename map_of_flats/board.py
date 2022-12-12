
import dash_leaflet as dl
from dash import Dash, dcc, html, Input, Output, State

# A few cities in Denmark.
cities = [dict(title="Aalborg", position=[57.0268172, 9.837735]),
          dict(title="Aarhus", position=[56.1780842, 10.1119354]),
          dict(title="Copenhagen", position=[55.6712474, 12.5237848])]
# Create example app.
app = Dash()
app.layout = html.Div([
    html.H1('Квартиры в Москве и МО'),
    html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='100%', height='600')
])

if __name__ == '__main__':
    app.run_server()