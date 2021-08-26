import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# Pandas
import pandas as pd

data_raw = pd.read_csv('./data/asesor.csv',
                       parse_dates=['Cosecha_Liquidacion', 'Fecha_Ingreso_Operacion', 'Fecha_retiro',
                                    'FechaNacimiento'], encoding='Latin1')
data_encuesta = pd.read_csv('data/encuesta.csv', parse_dates=['FechaRegistro', 'Fecha_Retiro'], encoding='Latin1')

# Renames encuesta.csv DF index columns to match asesor.cv's
df_encuesta_renamed = data_encuesta.rename(columns={'id_Usuario': 'IdFuncionario'})
df_encuesta_renamed['Renuncio'] = 1

# Merges asesor.csv and encuesta.csv on IdFuncionario columns to get the employees that no longer work for the company
merged_asesor = data_raw.merge(df_encuesta_renamed, how='left', on='IdFuncionario')

# Fills empty cells on "Renuncio" to 0 in order to indicate employees that are working for the company.
merged_asesor['Renuncio'].fillna(0, inplace=True)

esta = merged_asesor[merged_asesor['Renuncio'] == 0]
no_esta = merged_asesor[merged_asesor['Renuncio'] == 1]

esta_grouped = esta.groupby('Cosecha_Liquidacion').sum().reset_index()
no_esta_grouped = no_esta.groupby('Cosecha_Liquidacion').sum().reset_index()

merged_asesor.sort_values(by=['IdFuncionario', 'Fecha_retiro'], inplace=True)
df_unique = merged_asesor[merged_asesor.duplicated(subset=['IdFuncionario'], keep='last')]
df_unique.reset_index(drop=True, inplace=True)
columns_names = df_unique.columns

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
                    dcc.Graph(id="count_estrato", figure=px.histogram(merged_asesor, x="Estrato"))
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

        ], className="col-10")

    ], className="row")

    # dcc.Graph(id="count_num_rot", figure=px.histogram(merged_asesor, x="num_rot")),
    # dcc.Graph(id="count_edad", figure=px.histogram(merged_asesor, x="Edad"))
], className="container")
