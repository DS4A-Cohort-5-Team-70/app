import dash_core_components as dcc
import dash_html_components as html

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
                html.H4("ID", className="col-4"),
                html.H4("Nombre", className="col-4"),
                html.H4("Probabilidad", className="col-4"),
            ], className="row")

        ], className="col-10"),
    ], className="row")
], className="container")
