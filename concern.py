import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app import app, historical_data

approval_polls = pd.read_csv('covid_approval_polls.csv')
approval_polls_adj = pd.read_csv('covid_approval_polls_adjusted.csv')
approval_toplines = pd.read_csv('covid_approval_toplines.csv')
concern_polls = pd.read_csv('covid_concern_polls.csv')
concern_polls_adj = pd.read_csv('covid_concern_polls_adjusted.csv')
concern_toplines = pd.read_csv('covid_concern_toplines.csv')

concern_vals = ['end_date','very', 'somewhat', 'not_very', 'not_at_all']

data = concern_polls.copy()

data.loc[data.subject == 'concern-economy', 'subject'] = 'economy'
data.loc[data.subject == 'concern-infected', 'subject'] = 'infected'
# data['end_date'] = pd.to_datetime(data['end_date']).dt.date


concern_US_layout = html.Div([
    html.H4("Category"),
    dcc.Dropdown(
        id="concern",
        options=[{'label': 'Economy', 'value': 'economy'},
                {'label': 'COVID Infection', 'value': 'infected'}],
        multi=False,
        value="economy"
    ),
    html.Br(),
    dcc.Graph(id='line_plot5', figure={})
])


@app.callback(
    [Output(component_id='line_plot5', component_property='figure')],
    [Input(component_id='concern', component_property='value')]
)

def update_graph(concern):

    d = data[data['subject'] == concern]

    c = "Economy" if concern == "economy" else "COVID Infection"
    sub = "How concerned Americans say they are about the coronavirus’s effect on the U.S. economy?" if concern == "economy" else "How concerned Americans say they are that they, someone in their family or someone else they know will become infected with the coronavirus?"

    df = pd.melt(d[concern_vals], id_vars= ['end_date'])

    fig = px.line(df, x='end_date', y='value',color='variable', 
                # trendline="expanding",
                # trendline="rolling", trendline_options=dict(window=35),
            # trendline="lowess", trendline_options=dict(frac=0.1),
        color_discrete_sequence= px.colors.diverging.Temps,
        title = f"Overview of {c} Concern Levels <br><sup>{sub}</sup>",
        labels=dict(end_date="Date", variable="Concern Level", value = "Percentage"))
    #fig.update_layout(xaxis_title = 'Date',  font_size = 15)

    return [go.Figure(data=fig)]

