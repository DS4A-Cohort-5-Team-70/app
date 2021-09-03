import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# plotly
import plotly.express as px

from app import app
from views import home, prediction, navbar, detail

content = html.Div(id="page-content")

url_bar_and_content_div = html.Div([dcc.Location(id="url"), navbar.sidebar, content])

app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    navbar.sidebar_header,
    navbar.sidebar,
    home.main_view,
    detail.details_page
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
        return detail.details_page
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

""" @app.callback(
    Output("histogram", "figure"),
    [Input("x_value", "value")])
def update_chart(x_value):
    fig = px.histogram(home.unique_employees_df, x=x_value, color="lineanegocio")
    return fig  """

@app.callback(
    Output("main_histogram", "figure"),
    Output("pie_renuncia", "figure"),
    Output("count_edad", "figure"),
    Output("count_canal", "figure"),
    Output("count_hijos", "figure"),
    Output("count_segmento", "figure"),
    Output("count_renuncio", "figure"),
    Output("count_comision", "figure"),
    Output("count_lineanegocio", "figure"),
    Output("employee_number", "children"),
    Input("age_slider", "value"), 
    Input("x_value", "value"),)
def update_df(age_slider, x_value):
    filtered_unique_df = home.unique_employees_df.query('{} < edad < {}'.format(age_slider[0], age_slider[1]))
    filtered_grouped_df = home.grouped_df.query('{} < edad < {}'.format(age_slider[0], age_slider[1]))
    main_histogram = px.histogram(filtered_unique_df, x=x_value, color="lineanegocio")
    pie_renuncia = px.pie(filtered_unique_df, names='renuncio', title='Porcentaje de renuncia')
    count_edad=px.histogram(filtered_unique_df, x="edad")
    count_canal = px.histogram(filtered_unique_df, x="canal")
    count_hijos=px.histogram(filtered_unique_df, x="cantidadhijos")
    count_segmento=px.histogram(filtered_unique_df, x="segmento")
    count_renuncio = px.histogram(filtered_unique_df, x="renuncio")
    count_comision = px.line(filtered_unique_df, x='idfuncionario', y='vr_comision', color=filtered_unique_df["renuncio"])
    count_lineanegocio=px.histogram(filtered_unique_df, x="lineanegocio")
    employee_number = filtered_unique_df.shape[0]
    return main_histogram, pie_renuncia, count_edad, count_canal, count_hijos, \
    count_segmento, count_renuncio,count_comision, count_lineanegocio, employee_number


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
