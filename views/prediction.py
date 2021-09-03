import dash_core_components as dcc
import dash_html_components as html
import dash_table
from . import home
import pickle

PAGE_SIZE = 20
#random_forest = pickle.load(open('./finalized_model.sav', 'rb'))
page_2 = html.Div([
    # id, nombre, prob
    html.Div([

        html.Div([html.Label('Estimaciones'),
                  dcc.RadioItems(
                      options=[
                          {'label': '1 mes', 'value': 'NYC'},
                          {'label': u'2 meses', 'value': 'MTL'},
                          {'label': '3 meses', 'value': 'SF'}
                      ],
                      value='MTL'
                  ),
                  ], className="col-2"),

        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                    ],
                    data=home.unique_employees_df.to_dict('records'),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                ),
                html.Div(id='datatable-interactivity-container')
            ], className="row")

        ], className="col-10"),
    ], className="row")
], className="container")


