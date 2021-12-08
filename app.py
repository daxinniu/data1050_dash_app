import dash
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
app = dash.Dash(__name__)


app.layout = html.Div([
    html.H2("COVID Data Visualization"),
    html.H4("State"),
    dcc.Dropdown(
        id="state",
        options=[{'label': i, 'value': i} for i in np.sort(historical_data.State.unique()) ],
        multi=False,
        value="RI"
    ),
    html.H4("Option"),
    dcc.Dropdown(
        id="option",
        options=[{'label': i, 'value': i} for i in historical_data.columns[4:] ],
        multi=False,
        value="Number of Cases"
    ),
    html.Br(),
    dcc.Graph(id='line_plot', figure={})
    # html.H4("Values"),
    # dcc.Dropdown(
    #     id="values-dropdown",
    #     options=[{'label': i, 'value': i} for i in df.columns],
    #     multi=False,
    #     value="Element"
    # ),
    # html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    # dash_table.DataTable(
    # id='table',
    # columns=[{"name": i, "id": i} for i in df3.columns],
    # data=df3.to_dict('records'),
    # )
])


@app.callback(
    [Output(component_id='line_plot', component_property='figure')],
    [Input(component_id='option', component_property='value')]
)
def update_graph( option_val):
    
    # Plotly Express
    fig = px.line(historical_data, x='Date', y= option_val , color = 'State', title = f"{option_val} Overview")
    
    return [go.Figure(data=fig)]


# @app.callback([
#     # Output('table', 'data'),
#     # Output('table', 'columns')
#     # ], 
#     # [
#     #     Input('submit-button-state', 'n_clicks'),
#     #     State('index-dropdown', 'value'),
#     #     State('columns-dropdown', 'value'),
#     #     State('values-dropdown', 'value'),
#     ])

# def update_cols(n_clicks, index_val, columns_val, values_val):
#     if index_val == columns_val or index_val == values_val or values_val == columns_val:
#         print("Inputs must all be different!")
#         return None, None
#     temp = df.pivot_table(
#         index=index_val,
#         columns=columns_val, 
#         values=values_val,
#         aggfunc=identity,
#     )
#     out_df = pd.DataFrame(temp.to_records())
#     out_cols = [{"name": i, "id": i} for i in out_df]
#     return out_df.to_dict('records'), out_cols

if __name__ == '__main__':
    app.run_server(debug=True)