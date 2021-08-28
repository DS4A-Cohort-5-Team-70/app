import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

categories = ['Cumplimiento', 'Ausentismo', 'UCN',
              'Comisión', 'Tiempo Útil']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[1, 5, 2, 2, 3],
    theta=categories,
    fill='toself',
    name='Employee A'
))
fig.add_trace(go.Scatterpolar(
    r=[4, 3, 2.5, 1, 2],
    theta=categories,
    fill='toself',
    name='Employee B'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )),
    showlegend=False
)

details_page = html.Div([
    html.Div([
        html.Div([
            html.H1("Florentino Ariza"),
            html.P("Resumen del empleado, detalles generados automáticamente"
                   " desde el set de datos"),
            html.Ul([
                html.Li("Dinero que ha generado a la compañía en últimos meses"),
                html.Li("Gastos de recontratación"),
                html.Li("Ahorros si se logra retención"),
                html.Li("Causa probable de renuncia (punto a negocioar para retención)"),
            ]),
            html.H4("Recomendación"),
            html.Span("Retener", className="badge badge-success"),
            html.Span("Dejar ir", className="badge badge-danger"),
        ], className="col"),
        html.Div([
            dcc.Graph(figure=fig)
        ], className="col")
    ], className="row align-items-center"),
], className="container")
