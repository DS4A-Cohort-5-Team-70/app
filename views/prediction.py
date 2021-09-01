import dash_core_components as dcc
import dash_html_components as html
import dash_table
from . import home
import pickle

PAGE_SIZE = 20
random_forest = pickle.load(open('./finalized_model.sav', 'rb'))
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
                    id='table-sorting-filtering',
                    columns=[
                        {'name': i, 'id': i, 'deletable': True} for i in sorted(home.df.columns)
                    ],
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='native',

                    filter_action='custom',
                    filter_query='',

                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[]
                )
            ], className="row")

        ], className="col-10"),
    ], className="row")
], className="container")

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3
