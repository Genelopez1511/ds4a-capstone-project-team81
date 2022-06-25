from cProfile import label
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn import datasets
from sklearn.cluster import KMeans

# Leer el dataset
hurtos_df = pd.read_csv('/mnt/c/Users/Génesis/Documents/GitHub/ds4a-capstone-project-team81/data/hurto_a_persona.csv', encoding='utf-8')
consolidado_df = pd.read_csv('/mnt/c/Users/Génesis/Documents/GitHub/ds4a-capstone-project-team81/data/consolidado_cantidad_casos_criminalidad_por_anio_mes.csv', encoding='utf-8')
print(hurtos_df.head())


# Le doy nombre a app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Comienzo a crear el layout
app.layout = html.Div(children = [
    html.H1("Analysis of crime data in Medellin, Colombia.", style={'text-align': 'center'}),
    html.P(
            """Select different days using the date picker or by selecting
            different time frames on the histogram."""),
    dcc.Tabs(
        id = 'tabs',
        value = 'statistics',
        children = [
            dcc.Tab(
                id = 'statistics',
                value = 'statistics',
                label = 'Statistics',
                children = [
                    # column for user controls
                    html.Div(
                        className= "four columns",
                        children = [
                    # Div de feccha 
                        html.Div(
                            className = 'row',
                            children = 
                            [
                                dbc.Label("Select a date:  ", className="mr-2"),
                                dcc.DatePickerSingle(
                                    id = 'date-picker-single',
                                    min_date_allowed = dt(2003, 1, 1),
                                    max_date_allowed = dt(2021, 9, 1),
                                    initial_visible_month = dt(2021, 1, 1),
                                    date = str(dt(2021, 1, 1)),
                                    display_format = 'YYYY-MM-DD',
                                    style={"border": "0px solid black"}
                                )
                            ]

                        ),
                        # div de barrio
                        html.Div(
                            className = 'row',
                            children =
                            [
                                dbc.Label("Select a neighborhood:  ", className="mr-2"),
                                dcc.Dropdown(
                                    id = 'neighborhood',
                                    options = [{'label': i, 'value': i} for i in hurtos_df['nombre_barrio'].unique()],
                                    multi=True,
                                    value = [],
                                    placeholder = 'Select a neighborhood'
                                
                                )
                            ]
                        ),
                        # div de tiempo
                        html.Div(
                            className = 'row',

                            children =
                            [
                                dbc.Label("Select a time:  ", className="mr-2"),
                                dcc.Dropdown(
                                    id = 'time',
                                    options = [
                                        {
                                            "label": str(n) + ":00",
                                            "value": str(n),
                                        }
                                        for n in range(24)
                                    ],
                                    multi=True,
                                    placeholder = 'Select a time'
                                    
                                )
                            
                            ],
                        ),
                        # Anotaciones de fuente
                        dcc.Markdown(
                            # """
                            # Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)
                            # Links: [Source Code](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-uber-rides-demo) | [Enterprise Demo](https://plotly.com/get-demo/)
                            # """
                        ),
                        #graficos
                        dcc.Graph(
                            figure={
                                'data': [
                                    { }
                                ]
                            }

                        )


                    ]
                ),

            ]
        ),
        # se crea la segunda pestaña model
        dcc.Tab(
        id = 'model',
        value = 'model',
        label = 'Model',
        children = [
            html.Div(
            id = 'div_model',
            children = [
                html.H3("Model Team 81"),]
                        )
                    ]
            )
    ]
    )
])

if __name__ == '__main__':
    app.run_server(app.run_server(host='127.0.0.1',port='8050',debug=True))