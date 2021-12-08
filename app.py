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
from pull_data import pull_data
from pull_data import clean_data

# Load Data
URL = "https://api.covidactnow.org/v2/states.csv?apiKey=bd3dfdfc355042c0996d60494588c092"
historical = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=bd3dfdfc355042c0996d60494588c092"

historical_data = pull_data(historical)
historical_data = clean_data(historical_data)


#APP
app = dash.Dash(__name__ , suppress_callback_exceptions=True , external_stylesheets=[dbc.themes.LUX])




