from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

stylesheets = ["./assets/style/style.css"]
# scripts = ["./assets/js/main.js"]
# app = Dash(__name__, external_stylesheets=stylesheets, external_scripts=scripts)
app = Dash(__name__, external_stylesheets=stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("desmatamento-alt-final.csv")

dfe = pd.read_csv("desmatamento-estado.csv")
dfe = dfe.sort_values(by="area km²", ascending=False)


# figbar = px.bar(dfe, x="uf",  y="area km²", text_auto='.2s')
figbar = px.bar(df, x="Estado", y="Area-Total-Km")

figpie = px.pie(df, values="Area-Desmatada-Km", names="Nome-Regiao")

figlines = px.line(df, y=['Area-Total-Km', 'Area-Desmatada-Km'], line_dash='Anos',
                   color='Anos')


fighis = px.histogram(df, y="Area-Desmatada-Km", x="Anos")


figros = px.pie(df, values="Area-Total-Km", names="Estado",
                color_discrete_sequence=px.colors.sequential.RdBu,
                opacity=0.7, hole=0.5)


opcoes = list(df['Estado'].unique())


opcoes.append("Todos Estados")


app.layout = html.Div(children=[
    html.H1(children='Desmatamento Amazônica e Mata Atlântica', id="Titulo"),
    html.H2(children='Contem apenas Estados que contem mata atlântica',
            id="Explicacao1"),
    html.H3(children='Municipios com indice de desmatamento menor que 0,1 km não foram computados', id="Explicacao2"),
    html.Div(id="sel", children='''
        Selecione o Municipio desejado
    '''),

    html.Div(id="texto"),




    dcc.Dropdown(opcoes, value='Todos Estados', id='select-Municipio'),


    dcc.Graph(

        id='Grafico',
        figure=figbar
    ),
    dcc.Graph(
        id="Pie",
        figure=figpie
    ),
    dcc.Graph(
        id="Lines",
        figure=figlines
    ),
    dcc.Graph(
        id="Histograma",
        figure=fighis
    ),
    dcc.Graph(
        id="Rosca",
        figure=figros
    ),


])


@callback(
    Output('Grafico', 'figure'),
    Input('select-Municipio', 'value'),
)
def barras(value):
    if value == "Todos Estados":
        figbar = px.bar(dfe, x="uf",  y="area km²")

    else:
        tabela_filtrada = df.loc[df['Estado'] == value, :].sort_values(
            by="Area-Desmatada-Km", ascending=False)
        figbar = px.bar(tabela_filtrada, x="Municipio",  y="Area-Desmatada-Km")

    return figbar


@callback(
    Output('Pie', 'figure'),
    Input('select-Municipio', 'value'),
)
def pizza(value):
    if value == "Todos Estados":
        figpie = px.pie(df, values="Area-Desmatada-Km", names="Nome-Regiao")

    else:
        tabela_filtrada = df.loc[df['Estado'] == value, :].sort_values(
            by="Area-Desmatada-Km", ascending=False)
        figpie = px.pie(tabela_filtrada,
                        values="Area-Desmatada-Km", names="Nome-Regiao")

    return figpie


@callback(
    Output('Lines', 'figure'),
    Input('select-Municipio', 'value'),
)
def linha(value):
    if value == "Todos Estados":
        figlines = px.line(df, y=['Area-Total-Km', 'Area-Desmatada-Km'], line_dash='Anos',
                           color='Anos')

    else:
        tabela_filtrada = df.loc[df['Estado'] == value, :].sort_values(
            by="Area-Desmatada-Km", ascending=False)
        figlines = px.line(tabela_filtrada, y=['Area-Total-Km', 'Area-Desmatada-Km'], line_dash='Anos',
                           color='Anos')

    return figlines


@callback(
    Output('Histograma', 'figure'),
    Input('select-Municipio', 'value'),
)
def histograma(value):
    if value == "Todos Estados":
        fighis = px.histogram(df, y="Area-Desmatada-Km", x="Anos")

    else:
        tabela_filtrada = df.loc[df['Estado'] == value, :].sort_values(
            by="Area-Desmatada-Km", ascending=False)
        fighis = px.histogram(tabela_filtrada, y="Area-Desmatada-Km", x="Anos")

    return fighis


@callback(
    Output('Rosca', 'figure'),
    Input('select-Municipio', 'value'),

)
def rosca(value):
    if value == "Todos Estados":
        figros = px.pie(df, values="Area-Total-Km", names="Estado",
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        opacity=0.7, hole=0.5)

    else:
        tabela_filtrada = df.loc[df['Estado'] == value, :].sort_values(
            by="Area-Desmatada-Km", ascending=False)
        figros = px.pie(tabela_filtrada, values="Area-Total-Km", names="Estado",
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        opacity=0.7, hole=0.5)

    return figros


figlines.update_layout(title='<b>Desmatamento</b>')
figbar.update_layout(title='<b>Desmatamento</b>')
figpie.update_layout(title='<b>Desmatamento</b>')
figros.update_layout(title='<b>Desmatamento</b>')
fighis.update_layout(title='<b>Desmatamento</b>')

if __name__ == '__main__':
    app.run_server(debug=True)
