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

Cases = ['Date', 'Number of Cases', 'Number of Deaths',
        'Number of Positive Tests', 'Number of New Cases',
        'Number of New Deaths']
Vaccines = ['Date','Number of Vaccines Distributed', 'Number of Vaccinations Initiated',
       'Number of Vaccinations Completed', 'Number of Vaccines Administered']
Hospitalization = ['Date','Hospital Beds Capacity',
        'Hospital Beds Current Usage Total',
       'Hospital Beds Current Usage Covid', 
       'ICU Beds Capacity', 'ICU Beds Current Usage Total',
       'ICU Beds Current Usage Covid']
Metrices = ['Date','Test Positivity Ratio','Test Positivity Ratio',
       'Contact Tracer Capacity Ratio', 'Infection Rate',
       'Infection Rate CI90', 
       'ICU Capacity Ratio', 
       'Vaccinations Initiated Ratio',
       'Vaccinations Completed Ratio']



approvals = approval_polls.sort_values('start_date')
df = approvals.groupby(['start_date', 'subject']).sum()
df = df.loc[:, df.columns != 'sample_size']
df = df.reset_index()
df['approve'] = round(df['approve'], 2)
df['disapprove'] = round(df['disapprove'], 2)
df.sort_values(['subject', 'start_date'])

hitorical_total = historical_data.groupby('Date').sum().reset_index()

approve_combine = pd.merge(hitorical_total, df,  how='right', left_on='Date', right_on='start_date')
approve_combine.sort_values('Date')


df = approve_combine



Approval_US_layout = html.Div([
    html.H4("President"),
    dcc.Dropdown(
        id="president",
        options=[{'label': i, 'value': i} for i in np.sort(df.subject.unique()) ],
        multi=False,
        value="Biden"
    ),
    html.Br(),
    html.H4("METRIC CATEGORY"),
    dcc.Dropdown(
        id="option3",
        options=[{'label': "Cases", 'value': 'Cases'},
                 {'label': 'Hospitalization', 'value': 'Hospitalization'},
                 {'label': 'Metrices', 'value': 'Metrices'} ,
                 {'label': "Vaccination", 'value': 'Vaccines'}],
        multi=False,
        value= 'Cases'
    ),
    html.Br(),
    dcc.Graph(id='line_plot3', figure={})
])


@app.callback(
    [Output(component_id='line_plot3', component_property='figure')],
    [Input(component_id='president', component_property='value'),
     Input(component_id='option3', component_property='value')
    ]
)
def update_graph(president_val, option_val):
    
    choice_vals = Metrices + ['subject', 'approve', 'disapprove']
    choice_vals = np.sort(choice_vals)

    if option_val == 'Cases':
        choice_vals = Cases + ['subject', 'approve', 'disapprove']
        choice_vals = np.sort(choice_vals)
        data = df[choice_vals]


    elif option_val == 'Vaccines':
        choice_vals = Vaccines + ['subject', 'approve', 'disapprove']
        choice_vals = np.sort(choice_vals)
        data = df[choice_vals]

    elif option_val == 'Hospitalization':
        choice_vals = Hospitalization + ['subject', 'approve', 'disapprove']
        choice_vals = np.sort(choice_vals)
        data = df[choice_vals]

    elif option_val == 'Metrices':
        choice_vals = Metrices + ['subject', 'approve', 'disapprove']
        choice_vals = np.sort(choice_vals)
        data = df[choice_vals]    
    
    
    app_melt = pd.melt(data, id_vars= ['Date', 'subject'])
    fig = px.line(app_melt[app_melt['subject'] == president_val], x='Date', y='value',color='variable', title = f"Overview of Choice of President {president_val}")

    return [go.Figure(data=fig)]