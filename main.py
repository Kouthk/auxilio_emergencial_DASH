# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
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

#Grafico2
fig2= px.pie(df, values="Valor a Ser Repassado", names="UF", title="Valor repassado por estado")


#Grafico3
fig3 = px.imshow(df, x="Unidade Territorial", y="Pessoas ELegiveis a receber R$150")



app.layout = html.Div(children=[
    html.H1(children='Auxilio Emergencial - 2021'),
    html.Div(children='''
        Análise de dados com dataset referente ao Auxílio Emergencial no ano de  2021    
        '''),
    html.Br(),
    html.H3(
            children="Grafico de Barras: Pessoas Elegiveis por estado",
            style={ "margin": "1em 0 0 4.2em "}
    ),
    html.Div([
            dcc.Dropdown(opcoes, value="Todos os Estados", id='lista_estados_g2'),
        ], style={"width":"200px", "margin":"1em 0 0 5em "}

    ),
    dcc.Graph(
        id='Pessoas_elegiveis_estado',
        figure=fig1
    ),
    html.H3(children="Grafico de Pizza: Valor Elegivel por estado",
            style={ "margin": "1em 0 0 4.2em "}),
    html.Div([
        dcc.Dropdown(opcoes, value="Todos os Estados", id='lista_estados'),
    ], style={"width": "200px", "margin": "1em 0 0 5em "}
    ),
    html.H3(children="Grafico de Sccater: Valor Elegivel por estado",
            style={ "margin": "1em 0 0 4.2em "}),
    dcc.Graph(
        id='valor_repassado_estados1',
        figure=fig2
    ),
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
    Input('lista_estados', 'value')
)
def update_output(value):
    if (value == "Todos os Estados"):
        fig1 = px.bar(df, x="UF", y="Pessoas Elegiveis", barmode="group")
    else:
        update_dados = df.loc[df["UF"]==value, :]
        fig1 = px.bar(update_dados, x="UF", y="Pessoas Elegiveis", barmode="group")
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)
