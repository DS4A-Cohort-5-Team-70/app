from dash.dependencies import Input
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Br import Br
from dash_html_components.Label import Label

details_page = html.Div([
    html.Div([
        html.Div([
            html.Label(htmlFor="idfuncionario_input", children="Write an id"),
            html.Br(),
            dcc.Input(id="idfuncionario_input", type="text", placeholder="", className="form-control", value=988, debounce=True),
            html.H1("Employee Summary"),
            html.P("In this view we can see an abstract for each employee. On the right side of the page we have a radar plot which shows:"),
            html.Ul([
                html.Li("Weight of each relevant variable"),
                html.Li("Probability of turnover"),
            ]),
            html.H4("Recommendation"),
            html.Span("Retention", className="badge badge-success"),
        ], className="col"),
        html.Div([
            dcc.Graph(id="radar")
        ], className="col")
    ], className="row align-items-center"),
], className="container")
