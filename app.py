# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#Envioromental variables
import os
from dotenv import load_dotenv
#Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#plotly
import plotly.express as px
#Pandas
import pandas as pd
#Postgres SQL
import psycopg2 as pg
import pandas.io.sql as psql

#Creates dash app
app = dash.Dash(__name__, title='Prediction Model')

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

df = pd.read_csv('./data/asesor.csv',parse_dates=['Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'], encoding='Latin1')
df_encuesta = pd.read_csv('./data/encuesta.csv')
print(df.head())
print(df.info())

df.sort_values(by=['IdFuncionario', 'Fecha_retiro'], inplace=True)
df_unique = df[df.duplicated(subset=['IdFuncionario'], keep='last')]
df_unique.reset_index(drop=True, inplace=True)
column_names = df_unique.columns


# App layout --------------------------------------------------------------------------------------

app.layout = html.Div([
    html.H1('Employee turnover',
            style={
                    'textAlign': 'center',
                }
    ),

    html.H4('Variable count by segmento'
    ),

    dcc.Dropdown(
        id="x_value",
        options=[{"label": column, "value": column} for column in column_names],
        value=column_names[10],
        multi=False
    ),

    html.Br(),

    dcc.Graph(id="histogram")
])

# Callbacks -------------------------------------------------------------------------------------------

@app.callback(
    Output("histogram", "figure"), 
    Input("x_value", "value"))
def update_chart(x_value):
    fig = px.histogram(df_unique, x=x_value, color="Segmento")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')