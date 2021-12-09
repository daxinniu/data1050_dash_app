
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
#import dash_pivottable
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app import app, historical_data

all_state_graph_layout = html.Div([
    html.H4("Select"),
    dcc.Dropdown(
        id="option1",
        options=[{'label': i, 'value': i} for i in np.sort(historical_data.columns[4:]) ],
        multi=False,
        value="Number of Cases"
    ),
    html.Br(),
    dcc.Graph(id='line_plot1', figure={})
])


@app.callback(
    [Output(component_id='line_plot1', component_property='figure')],
    [Input(component_id='option1', component_property='value')]
)
def update_graph( option_val):
    
    # Plotly Express
    fig = px.line(historical_data, x='Date', y= option_val , color = 'State', title = f"{option_val} Overview")
    
    return [go.Figure(data=fig)]