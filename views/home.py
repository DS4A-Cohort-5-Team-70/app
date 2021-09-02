import dash_core_components as dcc
import dash_html_components as html
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

main_view = html.Div([

    html.Div([

        html.Div([
            html.Label('Empleado'),
            dcc.Dropdown(
                options=[
                    {'label': '54345', 'value': 'NYC'},
                    {'label': u'9742', 'value': 'MTL'},
                    {'label': '87567', 'value': 'SF'}
                ],
                value='MTL'
            ),

            html.Label('Multi-Select Dropdown'),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value=['MTL', 'SF'],
                multi=True
            ),

            html.Label('Radio Items'),
            dcc.RadioItems(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value='MTL'
            ),

            html.Label('Checkboxes'),
            dcc.Checklist(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value=['MTL', 'SF']
            ),

            html.Label('Text Input'),
            dcc.Input(value='MTL', type='text'),

            html.Label('Slider'),
            dcc.Slider(
                min=0,
                max=9,
                marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                value=5,
            ),
        ], className="col-2"),

        html.Div([
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
                        value=columns_names[6],
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
                    dcc.Graph(id="boxplot", figure=px.box(df, x="cosecha_liquidacion", y="meta_recaudo"))
                    , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_genero", figure=px.histogram(df.groupby('idfuncionario')['edad'].max().to_frame(), x="edad"))
                    , className="col-lg-6 col-sm-12")
            ], className="row"),

            html.Div([
                html.Div(
                    dcc.Graph(id="count_estado_civil", figure=px.histogram(df.groupby('idfuncionario')['canal'].max().to_frame(), x="canal"))
                    , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_hijos", figure=px.histogram(df.groupby('idfuncionario')['cantidadhijos'].max().to_frame(), x="cantidadhijos"))
                    , className="col-lg-6 col-sm-12"),
            ], className="row"),

            html.Div([
                html.Div(
                    dcc.Graph(id="count_estrato", figure=px.histogram(df, x="segmento"))
                    , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_cantidad_hijos", figure=px.histogram(df, x="renuncio"))
                    , className="col-lg-6 col-sm-12")
            ], className="row"),

            html.Div([
                html.Div(
                    dcc.Graph(id="count_vivienda", figure=px.line(df.groupby('idfuncionario')['vr_comision'].mean().to_frame().reset_index(), x="idfuncionario", y="vr_comision"))
                    , className="col-lg-6 col-sm-12"),
                html.Div(
                    dcc.Graph(id="count_academico", figure=px.histogram(df, x="lineanegocio"))
                    , className="col-lg-6 col-sm-12")
            ], className="row"),

            html.Div([
                html.Div(
                    dcc.Graph(id="count_estado", figure=px.histogram(df, x="idfuncionario"))
                    , className="col-lg-6 col-sm-12"),
            ], className="row"),

        ], className="col-10")

    ], className="row")

    # dcc.Graph(id="count_num_rot", figure=px.histogram(df, x="num_rot")),
    # dcc.Graph(id="count_edad", figure=px.histogram(df, x="Edad"))
], className="container")
