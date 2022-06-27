from cProfile import label

import time # Únicamente se utiliza para la generación aleatoria de datos en la gráfica de ejemplo

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from components.histogram import histogram

from datetime import datetime as dt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Leer el dataset
hurtos_df = pd.read_csv('/Users/juliand/Projects/DS4A/ds4a-capstone-project-team81/data/hurto_a_persona.csv', encoding='utf-8')
consolidado_df = pd.read_csv('/Users/juliand/Projects/DS4A/ds4a-capstone-project-team81/data/consolidado_cantidad_casos_criminalidad_por_anio_mes.csv', encoding='utf-8')
# hurtos_df = pd.read_csv('/mnt/c/Users/Génesis/Desktop/proyecto_DS4A/project_ds4a/data/hurto_a_persona.csv', encoding='utf-8')
# consolidado_df = pd.read_csv('/mnt/c/Users/Génesis/Desktop/proyecto_DS4A/project_ds4a/data/consolidado_cantidad_casos_criminalidad_por_anio_mes.csv', encoding='utf-8')
print(hurtos_df.head())

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Componentes necesarios para la construcción de nuestro tablero
# Basado en:
#   https://github.com/facultyai/dash-bootstrap-components/blob/main/examples/python/advanced-component-usage/navbars.py (Barra de logo)
#   https://dash-bootstrap-components.opensource.faculty.ai/examples/graphs-in-tabs/ (Pestañas)
#   https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/ (Gráfica con filtros)


# Le doy nombre a app y defino el tema a utilizar
# Se pueden ver ejemplos de más temas aquí: https://bootswatch.com/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Entry 1"),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

# this example that adds a logo to the navbar brand
logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Analysis of crime data in Medellin, Colombia.", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.correlation-one.com/data-science-for-all-colombia",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in ['el poblado', 'estadio', 'calasanz']
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in ['el poblado', 'estadio', 'calasanz']
                    ],
                    value="sepal width (cm)",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),  
            ]
        ),
    ],
    body=True,
)

# Contruímos el layout utilizando componentes para una mejor organización del código.
# app.layout = html.Div(
#     [logo]
# )

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        logo,
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="Statistics", tab_id="scatter"),
                dbc.Tab(label="Model", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


## Definimos los callbacks

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "scatter":
            # return dcc.Graph(figure=data["scatter"])
            h = histogram.Histogram('')
            h = histogram.Histogram('')
            return h
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}


# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks
# NOTA: No necesitamos este bucle, podemos referenciar el callback directamente al componente que escogimos (logo)
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

if __name__ == '__main__':
    app.run_server(app.run_server(host='127.0.0.1',port='8050',debug=True))