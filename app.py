# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import psycopg2 as pg
import pandas.io.sql as psql
from dotenv import load_dotenv

app = dash.Dash(__name__, title='Prediction Model')

server = app.server

#-------------------------------------------------------------------------------------
#Data import from Postgres

#Loads env variables
load_dotenv()
user = os.getenv('DB_MASTER_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_ENDPOINT')
database = 'raw'

#Creating the connection
engine = pg.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
#Preparing the data
df = psql.read_sql('SELECT * FROM asesor', engine)
df.sort_values(by=['idfuncionario', 'fecha_retiro'], inplace=True)
df_unique = df[df.duplicated(subset=['idfuncionario'], keep='last')]
df_unique.reset_index(drop=True, inplace=True)
colum_names = df_unique.columns


#--------------------------------------------------------------------------------------
#App layout

app.layout = html.Div(children=[
    html.H1('Employee turnover',
            style={
                    'textAlign': 'center',
                }
    ),

    html.H4('Variable count by segmento'),

    dcc.Dropdown(
        id="x_value",
        options=[{"label": x, "value": x} 
                 for x in colum_names],
        value=colum_names[10],
        multi=False
    ),

    html.Br(),

    dcc.Graph(id="histogram")
])

@app.callback(
    Output("histogram", "figure"), 
    Input("x_value", "value"))
def update_chart(x_value):
    fig = px.histogram(df_unique, x=x_value, color="segmento")
    """ fig.update_layout(
        paper_bgcolor = '#b1c2e6',
        plot_bgcolor = '#b1c2e6'
    ) """
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')