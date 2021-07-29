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

#df = pd.read_csv('./data/asesor.csv',parse_dates=['Cosecha_Liquidacion', 'Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'], encoding='Latin1')
#df_encuesta = pd.read_csv('./data/encuesta.csv')


data_raw = pd.read_csv('./data/asesor.csv',parse_dates=['Cosecha_Liquidacion', 'Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'], encoding='Latin1')
data_encuesta = pd.read_csv('data/encuesta.csv', parse_dates=['FechaRegistro', 'Fecha_Retiro'], encoding='Latin1')

#Renames encuesta.csv DF index column to match asesor.cv's
df_encuesta_renamed = data_encuesta.rename(columns={'id_Usuario': 'IdFuncionario'})
df_encuesta_renamed['Renuncio'] = 1

#Merges asesor.csv and encuesta.csv on IdFuncionario column to get the employees that no longer work for the company
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
    html.Div([
        dcc.Dropdown(
        id="x_value",
        options=[{"label": column, "value": column} for column in column_names],
        value=column_names[10],
        multi=False
    ), 
        html.Br()],
    className='four columns'),
    
    html.Br(),
    html.Br(),
    

    

    dcc.Graph(id="histogram"),

    #px.box(esta, x="Cosecha_Liquidacion", y="Cumpl_Individual")

    dcc.Graph(id="boxplot", figure=px.box(esta, x="Cosecha_Liquidacion", y="Cumpl_Individual")),

    dcc.Graph(id="count_genero", figure=px.histogram(merged_asesor, x="Genero")),
    dcc.Graph(id="count_estado_civil", figure=px.histogram(merged_asesor, x="EstadoCivil")),
    dcc.Graph(id="count_hijos", figure=px.histogram(merged_asesor, x="Hijos")),
    dcc.Graph(id="count_cantidad_hijos", figure=px.histogram(merged_asesor, x="CantidadHijos")),
    dcc.Graph(id="count_estrato", figure=px.histogram(merged_asesor, x="Estrato")),
    dcc.Graph(id="count_vivienda", figure=px.histogram(merged_asesor, x="TipoVivienda")),
    dcc.Graph(id="count_academico", figure=px.histogram(merged_asesor, x="NivelAcademico")),
    dcc.Graph(id="count_estado", figure=px.histogram(merged_asesor, x="Estado")),
    #dcc.Graph(id="count_num_rot", figure=px.histogram(merged_asesor, x="num_rot")),
    #dcc.Graph(id="count_edad", figure=px.histogram(merged_asesor, x="Edad"))
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