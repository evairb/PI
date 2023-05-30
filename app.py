from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

stylesheets = ["./assets/style/style.css"]
# scripts = ["./assets/js/main.js"]
# app = Dash(__name__, external_stylesheets=stylesheets, external_scripts=scripts)
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("desmatamento.csv")

dfe = pd.read_csv("desmatamento-estado.csv")
dfe = dfe.sort_values(by="area km²", ascending=False)
fig = px.bar(dfe, x="uf",  y="area km²", text_auto='.2s')
# fig = px.pie(dfe,dfe["uf"], dfe["area km²"])


opcoes = list(df['Estado'].unique())

opcoes.append("Todos Estados")


app.layout = html.Div(children=[
    html.H1(children='Desmatamento Mata Atlântica', id="Titulo"),
    html.H2(children='Contem apenas estados que contem mata atlântica',
            id="Explicacao1"),
    html.H3(children='Municipios com indice de desmatamento menor que 0,1 km não foram computados', id="Explicacao2"),
    
    html.Div(children=[html.Div(children='''
        Selecione o municipio desejado
         ''', id='select-Municipio-text'),
        dcc.Dropdown(opcoes, value='Todos Estados', id='select-Municipio')],id='seletor'),


    dcc.Graph(
        id='Grafico',
        figure=fig
    )

])


@app.callback(
    Output('Grafico', 'figure'),
    Input('select-Municipio', 'value')
)
def teste(value):
    if value == "Todos Estados":
        fig = px.bar(dfe, x="uf",  y="area km²")
        # fig = px.pie(dfe, dfe["uf"], dfe["area km²"])

    else:
        tabela_filtrada = df.loc[df['Estado'] == value, :].sort_values(
            by="Area Desmatada(km)", ascending=False)
        fig = px.bar(tabela_filtrada, x="Municipio",  y="Area Desmatada(km)")
        # fig = px.pie(tabela_filtrada, dfe["uf"], dfe["area km²"])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
