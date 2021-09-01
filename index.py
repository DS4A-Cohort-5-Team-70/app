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

@app.callback(
    Output("histogram", "figure"),
    [Input("x_value", "value")])
def update_chart(x_value):
    fig = px.histogram(home.df, x=x_value, color="lineanegocio")
    return fig

@app.callback(
    Output('table-sorting-filtering', 'data'),
    Input('table-sorting-filtering', "page_current"),
    Input('table-sorting-filtering', "page_size"),
    Input('table-sorting-filtering', 'sort_by'),
    Input('table-sorting-filtering', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = home.df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = prediction.split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
