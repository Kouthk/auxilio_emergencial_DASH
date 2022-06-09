# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("dataset_auxilioEmergencial_2021.csv")

#Aqui cria o grafico
fig1 = px.bar(df, x="UF", y="Pessoas Elegiveis", barmode="group")

opcoes = list(df['UF'].unique())
opcoes.append("Todos os Estados")
opcoes.sort()
#Grafico2
fig2= px.pie(df, values="Valor a Ser Repassado", names="UF", title="Valor repassado por estado")

#Grafico3
fig3 = px.scatter(df, x="UF", y="Pessoas ELegiveis a receber R$150")
fig3.update_xaxes(categoryorder='category ascending')

app.layout = html.Div(children=[
    html.H1(children='Auxilio Emergencial - 2021'),
    html.Div(children='''
        Análise de dados com dataset referente ao Auxílio Emergencial no ano de  2021    
        '''),
    html.Br(),
    #Primeiro Grafico aqui
    html.H3(
            children="Grafico de Barras: Pessoas Elegiveis por estado",
            style={ "margin": "1em 0 0 4.2em "}
    ),
    html.Div([
            dcc.Dropdown(opcoes, value="Todos os Estados", id='lista_estados_g1'),
        ], style={"width":"200px", "margin":"1em 0 0 5em "}

    ),
    html.Div([
        html.Button('Ordenar Alfabeticamente o Grafico', id='order_g1', n_clicks=0),
        html.Button('Resetar Grafico', id='reset_g1', n_clicks=0),
    ], id="botoes_g1"),
    html.Div([
        dcc.Dropdown(opcoes, value="Todos os Estados", id='lista_estados_g1_multi', multi=True),
    ], style={"width": "600px", "margin": "1em 0 0 5em "}
    ),
    dcc.Graph(
        id='Pessoas_elegiveis_estado',
        figure=fig1
    ),
    # Segundo Grafico aqui
    html.H3(children="Grafico de Pizza: Valor Elegivel por estado",
            style={ "margin": "1em 0 0 4.2em "}),
    html.Div([
        dcc.Dropdown(opcoes, value="Todos os Estados", id='lista_estados'),
    ], style={"width": "200px", "margin": "1em 0 0 5em "}
    ),
    dcc.Graph(
        id='valor_repassado_estados1',
        figure=fig2
    ),
    #Terceiro Grafico aqui
    html.H3(children="Grafico de a decidir: Valor Elegivel por estado",
            style={ "margin": "1em 0 0 4.2em "}),
    html.Div([
        dcc.Dropdown(opcoes, value="Todos os Estados", id='a_decidir'),
    ], style={"width": "200px", "margin": "1em 0 0 5em "}
    ),
    dcc.Graph(
        id="abc",
        figure=fig3
    )
])

@app.callback(
    Output('Pessoas_elegiveis_estado', 'figure'),
    Input('lista_estados_g1', 'value'),
    Input('order_g1', 'n_clicks'),
    Input('reset_g1', 'n_clicks'),
    Input('lista_estados_g1_multi', 'value')
)
def update_graph1(value, order_g1, reset_g1, lista_estados_g1_multi):
    triggered_id = ctx.triggered_id
    if triggered_id == 'order_g1':
        return displayClick()
    elif triggered_id == 'reset_g1':
        return resetDisplayG1()
    elif triggered_id == 'lista_estados_g1_multi':
        return compareCom(lista_estados_g1_multi)
    else:
        return update_estado(value)



def update_estado(value):
    if (value == "Todos os Estados"):
        fig1 = px.bar(df, x="UF", y="Pessoas Elegiveis", barmode="group")
    else:
        print(value)
        update_dados = df.loc[df["UF"]==value, :]
        print(update_dados)
        fig1 = px.bar(update_dados, x="UF", y="Pessoas Elegiveis", barmode="group")
    return fig1

def displayClick():
    return fig1.update_xaxes(categoryorder='category ascending')

def resetDisplayG1():
    fig1 = px.bar(df, x="UF", y="Pessoas Elegiveis", barmode="group")
    return fig1

def compareCom(dados):
    update_dados = df.loc[df["UF"].isin(dados)]
    fig1 = px.bar(update_dados, x="UF", y="Pessoas Elegiveis", barmode="group")
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)
