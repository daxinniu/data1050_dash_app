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

Cases = np.sort(['Date', 'Number of Cases', 'Number of Deaths',
        'Number of Positive Tests', 'Number of New Cases',
        'Number of New Deaths'])
Vaccines = np.sort(['Date','Number of Vaccines Distributed', 'Number of Vaccinations Initiated',
       'Number of Vaccinations Completed', 'Number of Vaccines Administered'])
Hospitalization = np.sort(['Date','Hospital Beds Capacity',
        'Hospital Beds Current Usage Total',
       'Hospital Beds Current Usage Covid', 
       'ICU Beds Capacity', 'ICU Beds Current Usage Total',
       'ICU Beds Current Usage Covid'])
Metrices = np.sort(['Date','Test Positivity Ratio','Test Positivity Ratio',
       'Contact Tracer Capacity Ratio', 'Infection Rate',
       'Infection Rate CI90', 
       'ICU Capacity Ratio', 
       'Vaccinations Initiated Ratio',
       'Vaccinations Completed Ratio'])


by_state_graph_layout = html.Div([
    html.H4("State"),
    dcc.Dropdown(
        id="state",
        options=[{'label': i, 'value': i} for i in np.sort(historical_data.State.unique()) ],
        multi=False,
        value="RI"
    ),
    html.Br(),
    html.H4("Metric Category"),
    dcc.Dropdown(
        id="option2",
        options=[{'label': "Cases", 'value': 'Cases'},
                 {'label': 'Hospitalization', 'value': 'Hospitalization'},
                 {'label': 'Metrices', 'value': 'Metrices'},
                 {'label': "Vaccination", 'value': 'Vaccines'} ],
        multi=False,
        value= 'Cases'
    ),
    html.Br(),
    dcc.Graph(id='line_plot2', figure={})
])


@app.callback(
    [Output(component_id='line_plot2', component_property='figure')],
    [Input(component_id='state', component_property='value'),
     Input(component_id='option2', component_property='value')
    ]
)
def update_graph(state_val, option_val):
    
    
    temp_df = historical_data[historical_data['State']== state_val]
    
    if option_val == 'Cases':
        temp_df = temp_df[Cases]
    elif option_val == 'Vaccines':
        temp_df = temp_df[Vaccines]
    elif option_val == 'Hospitalization':
        temp_df = temp_df[Hospitalization]
    elif option_val == 'Metrices':
        temp_df = temp_df[Metrices]


    melt_n = pd.melt(temp_df, id_vars = "Date")
    melt_n.columns = ['Date','option','value']
    fig = px.line(melt_n, x='Date', y='value', color='option', title = f"Overview of {option_val} in {state_val}" ,
    labels=dict(value="", option="")) 
    
    return [go.Figure(data=fig)]