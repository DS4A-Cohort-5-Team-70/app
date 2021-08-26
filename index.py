import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# plotly
import plotly.express as px

from app import app
from views import home, prediction, navbar

content = html.Div(id="page-content")

url_bar_and_content_div = html.Div([dcc.Location(id="url"), navbar.sidebar, content])

app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    navbar.sidebar_header,
    navbar.sidebar,
    home.main_view,
])


# Callbacks -------------------------------------------------------------------------------------------

# sidebar

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.main_view
    elif pathname == "/prediction":
        return prediction.page_2
    elif pathname == "/detail":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Plots

@app.callback(
    Output("histogram", "figure"),
    [Input("x_value", "value")])
def update_chart(x_value):
    fig = px.histogram(home.df_unique, x=x_value, color="LineaNegocio")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
