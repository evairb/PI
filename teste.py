from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv("desmatamento-alt-final.csv")

fig = go.Figure()
pd.set_option('display.max_columns', None)


fig = px.line(df, y=['Area-Total-Km', 'Area-Desmatada-Km'], line_dash='Anos',
              color='Anos')
fig.update_layout(title='<b>Desmatamento</b>')
fig = px.histogram(df, y="Area-Desmatada-Km", x="Anos")
fig = px.pie(df, values="Area-Desmatada-Km", names="Nome-Regiao")


fig = px.pie(df, values="Area-Total-Km", names="Estado",
             color_discrete_sequence=px.colors.sequential.RdBu,
             opacity=0.7, hole=0.5)


# showing the plot
fig.show()


# formatando como o dado do eixo Y irá aparecer ao interagir com o
# mouse na figura
# fig = px.line(x=dados_x, y=dados_y, title="Vendas x Ano",
#               height=400, width=1000, line_shape='spline')
# fig = px.line(df, y="Area-Total-Km")


# fig = px.pie(df, df["Anos"], df["Area-Total-Km"])
