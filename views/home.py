import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.H3 import H3
import plotly.express as px
import psycopg2 as pg
import os
from dotenv import load_dotenv
# Pandas
import pandas as pd

load_dotenv()
user = os.getenv('DB_MASTER_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_ENDPOINT')
db_name = 'raw'

engine = pg.connect("host={} dbname={} user={} password={}".format(host, db_name, user, password))

df = pd.read_sql('SELECT * FROM asesor', engine)
columns_names = df.columns

grouped_df = df.groupby('idfuncionario').mean().reset_index()
unique_employees_df = df.groupby('idfuncionario').max().reset_index()
#ages_array = unique_employees_df["edad"]
ages_array = [20, 25, 30, 35, 40, 45, 50, 55]
main_view = html.Div([

    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    html.H6("Edad", className="col-12 text-center"),
                    dcc.RangeSlider(
                        id="age_slider",
                        min=20,
                        max=55,
                        step=5,
                        marks={age:f'{age}' for age in ages_array},
                        value=[25, 35]
                    )], className="col-4"),
                html.Div([
                    html.H6("Number of employees", className="col-12 text-center align-middle"),
                    html.H4(id="employee_number", children=unique_employees_df.shape[0], className="col-12 text-center align-middle"),
                ])
            ], className="row justify-content-center align-items-center cool-card mb-4 p-2"),
            
            html.Div([

                html.Div(
                    html.H6('Select a filter')
                    , className="col-12 text-center mt-5"),

                html.Div([
                    dcc.Dropdown(
                        id="x_value",
                        options=[{"label": columns, "value": columns} for columns in columns_names],
                        value=columns_names[6],
                        multi=False)
                ], className='col-6'),
                html.Div([
                    html.Div(
                        dcc.Graph(id="main_histogram")
                        , className="col-12")
                ], className="row"),


                html.Div(
                    html.H3('Exploring the data')
                    , className="col-12 text-center"),

                html.Div([
                    html.Div(
                        dcc.Graph(id="pie_renuncia")
                        , className="col-lg-6 col-sm-12"),
                    html.Div(
                        dcc.Graph(id="count_edad")
                        , className="col-lg-6 col-sm-12")
                ], className="row"),

                html.Div([
                    html.Div(
                        dcc.Graph(id="count_canal")
                        , className="col-lg-6 col-sm-12"),
                    html.Div(
                        dcc.Graph(id="count_hijos")
                        , className="col-lg-6 col-sm-12"),
                ], className="row"),

                html.Div([
                    html.Div(
                        dcc.Graph(id="count_segmento")
                        , className="col-lg-6 col-sm-12"),
                    html.Div(
                        dcc.Graph(id="count_renuncio")
                        , className="col-lg-6 col-sm-12")
                ], className="row"),

                html.Div([
                    html.Div(
                        dcc.Graph(id="count_comision")
                        , className="col-lg-6 col-sm-12"),
                    html.Div(
                        dcc.Graph(id="count_lineanegocio")
                        , className="col-lg-6 col-sm-12")
                ], className="row"),

        ], className="row justify-content-center align-items-center cool-card"),

            

        ], className="col-12")

    ], className="row")

    # dcc.Graph(id="count_num_rot", figure=px.histogram(df, x="num_rot")),
    # dcc.Graph(id="count_edad", figure=px.histogram(df, x="Edad"))
], className="container")
