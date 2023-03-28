import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from flask import Flask
from sqlalchemy import create_engine

#Recoger los datos del servidor SQL
def cargaDataFrameFebrero():
    #Conexion a la BBDD del servidor mySQL
    dialect='mysql+pymysql://sistemesbd:bigdata2223@192.168.193.133:3306/alumnes'
    sql="SELECT * from David_Febrero "
    sqlEngine=create_engine(dialect)
    dbConnection = sqlEngine.connect()
    frame= pd.read_sql(sql, dbConnection)
    dbConnection.close()
    return frame

def cargaDataFrameMarzo():
    #Conexion a la BBDD del servidor mySQL
    dialect='mysql+pymysql://sistemesbd:bigdata2223@192.168.193.133:3306/alumnes'
    sql="SELECT * from David_Marzo "
    sqlEngine=create_engine(dialect)
    dbConnection = sqlEngine.connect()
    frame= pd.read_sql(sql, dbConnection)
    dbConnection.close()
    return frame

dfFebrero = cargaDataFrameFebrero()
dfMarzo = cargaDataFrameMarzo()

#Initialize the app
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'davidballester_plotlyREE'


#Ajustar los datos
xFebrero = dfFebrero['id']
#Con esto nos quedamos con todos los valores del df el de id y nos quedamos con el array con todos los valores en 1 dimension.
yFebrero = dfFebrero.drop(['id', 'Feb_23'], axis=1)

xMarzo = dfMarzo['id']
#Con esto nos quedamos con todos los valores del df el de id y nos quedamos con el array con todos los valores en 1 dimension.
yMarzo = dfMarzo.drop(['id', 'Mar_23'], axis=1)


#Navbar
navbar = dbc.Navbar(
    [dbc.NavbarBrand("Dashboard Futures Gas Natural", className="ms-1",style={'textAlign': 'center', 'padding-left':'5rem', 'padding-right':'2rem'})
    ],
    color="info",
    dark=True
)

'''
#Creación de las gráficas
graficaScatterFebrero=dcc.Graph(
    id='graficaScatterFebrero', 
    figure = {
        'data':[
            go.Scatter(
                x=xFebrero,
                y=yFebrero,
                mode='lines'
            )
        ],
        'layout':
            go.Layout(
                colorway=["#0E5FA0"],
                title='Predicción del precio de la gasolina en Febrero',
                xaxis = {'title':'Días'},
                yaxis = {'title':'Precio de la gasolina (USD)'},
                margin = {'l': 120}
            )
    }
)

graficaScatterMarzo=dcc.Graph(
    id='graficaScatterMarzo', 
    figure = {
        'data':[
            go.Scatter(
                x=xMarzo,
                y=yMarzo,
                mode='lines'
            )
        ],
        'layout':
            go.Layout(
                colorway=["#0E5FA0"],
                title='Predicción del precio de la gasolina en Marzo',
                xaxis = {'title':'Días'},
                yaxis = {'title':'Precio de la gasolina (USD)'},
                margin = {'l': 120}
            )
    }
)'''



#Creación de las gráficas
figFebrero = go.Figure()

#Se pone cada columna de yFrebrero como nueva trace del Figure
for col in yFebrero:
    figFebrero.add_trace(go.Scatter(x=xFebrero, y=yFebrero[col], mode='lines', name=col))

#Se le pone el layout
figFebrero.update_layout(
    title='Gas Natural Febrero',
    xaxis_title='Día',
    yaxis_title='Precio',
    margin=dict(l=150, r=50, t=50, b=50),
    height=500,
    width=800,
    legend=dict(orientation='v', yanchor='top', y=1, xanchor='right', x=1)
)


graficaScatterFebrero=dcc.Graph(
    id='graficaScatterFebrero', 
    figure = {
        'data': figFebrero.data,
        'layout': figFebrero.layout
    }
)



figMarzo = go.Figure()

#Se pone cada columna de yMarzo como nueva trace del Figure
for col in yMarzo:
    figMarzo.add_trace(go.Scatter(x=xMarzo, y=yMarzo[col], mode='lines', name=col))

#Se le pone el layout
figMarzo.update_layout(
    title='Gas Natural Marzo',
    xaxis_title='Día',
    yaxis_title='Precio',
    margin=dict(l=150, r=50, t=50, b=50),
    height=500,
    width=800,
    legend=dict(orientation='v', yanchor='top', y=1, xanchor='right', x=1)
)


graficaScatterMarzo=dcc.Graph(
    id='graficaScatterMarzo', 
    figure = {
        'data': figMarzo.data,
        'layout': figMarzo.layout
    }
)


#Visualización de los datos
app.layout =  html.Div(children=[
    navbar,
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(html.Div([graficaScatterFebrero]), width=5),
        dbc.Col(html.Div([graficaScatterMarzo]), width=5)
    ])
])

if __name__=='__main__':
    app.run_server()