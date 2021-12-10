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

# Cases = ['Date', 'Number of Cases', 'Number of Deaths',
#         'Number of Positive Tests', 'Number of Negative Tests',
#         'Contact Tracers']
# Vaccines = ['Date','Vaccines Distributed', 'Vaccinations Initiated',
#        'Vaccinations Completed']
# Hospitalization = ['Date','Hhospital Beds Capacity',
#         'Hospital Beds Current Usage Total',
#        'Hospital Beds Current Usage Covid', 
#        'ICU Beds Capacity', 'ICU Beds Current Usage Total',
#        'ICU Beds Current Usage Covid']
Metrices = ['Date','Test Positivity Ratio',
       'Contact Tracer Capacity Ratio', 'Infection Rate',
       'Infection Rate CI90', 
       'ICU Capacity Ratio', 'Risk Levels Overall',
       'Vaccinations Initiated Ratio',
       'Vaccinations Completed Ratio']



approvals = approval_polls.sort_values('start_date')
df = approvals.loc[approvals['party']== 'all', :]


hitorical_total = historical_data.groupby('Date').sum().reset_index()
hitorical_total = hitorical_total[Metrices] 

approve_combine = pd.merge(hitorical_total, df, left_on='Date', right_on='start_date')
approve_combine.sort_values('Date')

choice_vals = Metrices + ['subject', 'approve', 'disapprove']
approve_combine = approve_combine[choice_vals]
app_melt = pd.melt(approve_combine, id_vars= ['Date', 'subject'])



#second graph
toplines = approval_toplines.copy()
toplines['timestamp'] = pd.to_datetime(toplines['timestamp'], errors='coerce').dt.date
toplines = toplines.drop('modeldate', axis = 1)

appro_party = pd.melt(toplines, id_vars= ['timestamp', 'subject','party'])

appro_party.loc[appro_party.party == "D", "party"] = "Democrats"
appro_party.loc[appro_party.party == "R", "party"] = "Republicans"
appro_party.loc[appro_party.party == "I", "party"] = "Independents"

parties = list(appro_party.party.unique())
parties.remove('all')

Approval_US_layout = html.Div([
    html.H4("President"),
    dcc.Dropdown(
        id="president1",
        options=[{'label': i, 'value': i} for i in np.sort(df.subject.unique()) ],
        multi=False,
        value="Biden"
    ),
    html.Br(),
    dcc.Graph(id='line_plot3', figure={}),


    html.H4("Party"),
    dcc.Dropdown(
        id="party",
        options=[{'label': i, 'value': i} for i in parties],
        multi=False,
        value="Democrats"
    ),
    
    html.Br(),
    html.H4("President"),
    dcc.Dropdown(
        id="president2",
        options=[{'label': i, 'value': i} for i in np.sort(appro_party.subject.unique())],
        multi=False,
        value= 'Biden'
    ),
    html.Br(),
    dcc.Graph(id='line_plot4', figure={})

])


@app.callback(
    [Output(component_id='line_plot3', component_property='figure'),
    Output(component_id='line_plot4', component_property='figure')
    ],

    [Input(component_id='president1', component_property='value'),
     Input(component_id='party', component_property='value'),
     Input(component_id='president2', component_property='value')
    ]
)
def update_graph(president1, party_val, president2):

    #figure1
    fig = px.line(app_melt[app_melt['subject'] == president1], x='Date', y='value',color='variable', 
    title = f"Overview of Choice of President {president1} approval rate compare to other metrics")
    
    ##figure2   
    df1 = appro_party[appro_party['subject'] == president2]
    df1 = df1[df1['party'] == party_val]
    fig1 = px.line(df1, x='timestamp', y='value',color='variable',
            title = f"Overview of Choice of '{party_val}' Party for President {president2}",
            labels=dict(timestamp="Date", value=" "))
   
    

    return [go.Figure(data=fig),go.Figure(data=fig1)]

