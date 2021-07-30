# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#Envioromental variables
import os
from dash_html_components.Div import Div
from dotenv import load_dotenv
#Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
#plotly
import plotly.express as px
import seaborn as sns
#Pandas
import pandas as pd
#Postgres SQL
import psycopg2 as pg
import pandas.io.sql as psql

#Creates dash app
app = dash.Dash(
    __name__, 
    title='Prediction Model',  
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

#Uses app's Flask server
server = app.server

# Getting the data -------------------------------------------------------------------------------------

#Loads env variables
load_dotenv()
user = os.getenv('DB_MASTER_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_ENDPOINT')
database = 'raw'

#Creating the connection
engine = pg.connect("host={} dbname={} user={} password={}".format(host, database, user, password))

#Preparing the data
#df = psql.read_sql('SELECT * FROM asesor', engine)

#df = pd.read_csv('./data/asesor.csv',parse_dates=['Cosecha_Liquidacion', 'Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'], encoding='Latin1')
#df_encuesta = pd.read_csv('./data/encuesta.csv')


data_raw = pd.read_csv('./data/asesor.csv',parse_dates=['Cosecha_Liquidacion', 'Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'], encoding='Latin1')
data_encuesta = pd.read_csv('data/encuesta.csv', parse_dates=['FechaRegistro', 'Fecha_Retiro'], encoding='Latin1')

#Renames encuesta.csv DF index columns to match asesor.cv's
df_encuesta_renamed = data_encuesta.rename(columns={'id_Usuario': 'IdFuncionario'})
df_encuesta_renamed['Renuncio'] = 1

#Merges asesor.csv and encuesta.csv on IdFuncionario columns to get the employees that no longer work for the company
merged_asesor = data_raw.merge(df_encuesta_renamed, how='left', on='IdFuncionario')

#Fills empty cells on "Renuncio" to 0 in order to indicate employees that are working for the company.
merged_asesor['Renuncio'].fillna(0, inplace=True)

esta = merged_asesor[merged_asesor['Renuncio'] == 0]
no_esta = merged_asesor[merged_asesor['Renuncio'] == 1]

esta_grouped = esta.groupby('Cosecha_Liquidacion').sum().reset_index()
no_esta_grouped = no_esta.groupby('Cosecha_Liquidacion').sum().reset_index()


merged_asesor.sort_values(by=['IdFuncionario', 'Fecha_retiro'], inplace=True)
df_unique = merged_asesor[merged_asesor.duplicated(subset=['IdFuncionario'], keep='last')]
df_unique.reset_index(drop=True, inplace=True)
columns_names = df_unique.columns

# App layout --------------------------------------------------------------------------------------


# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H1("Employee turnover")),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Descripción del proyecto",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Inicio", href="/", active="exact"),
                    dbc.NavLink("Página 1", href="/page-1", active="exact"),
                    dbc.NavLink("Página 2", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

main_view = html.Div([
    
            html.Div([
                html.Div(
                    html.H3('An interactive plot')
                , className="col-12 text-center mb-3")   
            ], className="row justify-content-center"),

            html.Div([
                 html.Div([
                    dcc.Dropdown(
                    id="x_value",
                    options=[{"label": columns, "value": columns} for columns in columns_names],
                    value=columns_names[10],
                    multi=False)
                ], className='col-6')
            ], className="row justify-content-center"),
            
            html.Div([
                html.Div(
                    dcc.Graph(id="histogram")
                , className="col-12")   
            ], className="row"),

            html.Div([
                html.Div(
                    html.H3('Exploring the data')
                , className="col-12 text-center")   
            ], className="row justify-content-center"),

            html.Div([
                html.Div(
                    dcc.Graph(id="boxplot", figure=px.box(esta, x="Cosecha_Liquidacion", y="Cumpl_Individual"))
                , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_genero", figure=px.histogram(merged_asesor, x="Genero"))
                , className="col-lg-6 col-sm-12")        
            ], className="row"),

            html.Div([
                html.Div(
                    dcc.Graph(id="count_estado_civil", figure=px.histogram(merged_asesor, x="EstadoCivil"))
                , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_hijos", figure=px.histogram(merged_asesor, x="Hijos"))
                , className="col-lg-6 col-sm-12"),
            ], className="row"),

            html.Div([
                html.Div(
                    dcc .Graph(id="count_estrato", figure=px.histogram(merged_asesor, x="Estrato"))
                , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_cantidad_hijos", figure=px.histogram(merged_asesor, x="CantidadHijos"))
                , className="col-lg-6 col-sm-12")
            ], className="row"),
            
            html.Div([
                html.Div(
                    dcc.Graph(id="count_vivienda", figure=px.histogram(merged_asesor, x="TipoVivienda"))
                , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_academico", figure=px.histogram(merged_asesor, x="NivelAcademico"))
                , className="col-lg-6 col-sm-12")      
            ], className="row"),

            html.Div([
                html.Div(
                    dcc.Graph(id="count_estado", figure=px.histogram(merged_asesor, x="Estado"))
                , className="col-lg-6 col-sm-12"),       
            ], className="row"),
    
    #dcc.Graph(id="count_num_rot", figure=px.histogram(merged_asesor, x="num_rot")),
    #dcc.Graph(id="count_edad", figure=px.histogram(merged_asesor, x="Edad"))
], className="container")

content = html.Div(id="page-content")

url_bar_and_content_div = html.Div([dcc.Location(id="url"), sidebar, content])

app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    sidebar_header,
    sidebar,
    main_view,
])


# Callbacks -------------------------------------------------------------------------------------------

#sidebar

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return main_view
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


#Plots

@app.callback(
    Output("histogram", "figure"), 
    [Input("x_value", "value")])
def update_chart(x_value):
    fig = px.histogram(df_unique, x=x_value, color="Segmento")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')