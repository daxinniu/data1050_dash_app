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

approval_by_state = pd.read_csv('Biden_50_State_Approval_Registered_Voters_2021.csv')

dropcol = ['Politician', 'Demographic', 'Margin of error','Net Approval']

approval_by_state.drop(dropcol, inplace=True, axis=1)

code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}

approval_by_state['State'] = approval_by_state['State'].map(code)

approval_by_state = approval_by_state.rename(columns={'Fielding end':'Survey Date'})

    
# Plotly Express
fig = px.choropleth(approval_by_state,
            locations='State',
            color='Approve',
            color_continuous_scale='spectral_r',
            hover_name='State',
            locationmode='USA-states',
            labels={'Approval Rate by State'},
            scope='usa',
            animation_frame="Survey Date")

fig.add_scattergeo(
    locations=approval_by_state['State'],
    locationmode='USA-states',
    text=approval_by_state['State'],
    mode='text')

fig.update_layout(
title={'text':'Biden Approval Rate by State',
    'xanchor':'center',
    'yanchor':'top',
    'x':0.5})
    

map_layout = html.Div([
    html.Br(),
    dcc.Graph(figure=fig)
    ])