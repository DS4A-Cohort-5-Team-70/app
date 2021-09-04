import dash_core_components as dcc
import dash_html_components as html
import dash_table
from . import home
import pickle

# datable_df = home.unique_employees_df
datable_df = home.mockup_data
PAGE_SIZE = 20
pd = home.pd


def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0
    numeric_columns = ["idfuncionario", "probability"]
    if df_column in numeric_columns:
        return 'numeric'
    else:
        return 'text'


# random_forest = pickle.load(open('./finalized_model.sav', 'rb'))
page_2 = html.Div([
    # id, nombre, prob
    html.Div([
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": False, 'type': table_type(i), "selectable": True} for i in
                        datable_df
                    ],
                    data=datable_df.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="single",
                    page_action="native",
                    page_current=0,
                    page_size=10,
                ),
                html.Div(id='datatable-interactivity-container')
            ], className="row")

        ], className="col-12"),
    ], className="row")
], className="container")
