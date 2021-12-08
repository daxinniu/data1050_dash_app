import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_pivottable
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')
def identity(x): return x

df2 = df.pivot_table(
    index='Period',
    columns='Group', 
    values='Element',
    aggfunc=identity,
)
df3 = pd.DataFrame(df2.to_records())

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H2("Pivot Table"),
    html.H4("Index"),
    dcc.Dropdown(
        id="index-dropdown",
        options=[{'label': i, 'value': i} for i in df.columns],
        multi=False,
        value="Period"
    ),
    html.H4("Columns"),
    dcc.Dropdown(
        id="columns-dropdown",
        options=[{'label': i, 'value': i} for i in df.columns],
        multi=False,
        value="Group"
    ),
    html.H4("Values"),
    dcc.Dropdown(
        id="values-dropdown",
        options=[{'label': i, 'value': i} for i in df.columns],
        multi=False,
        value="Element"
    ),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df3.columns],
    data=df3.to_dict('records'),
    )
])

@app.callback([
    Output('table', 'data'),
    Output('table', 'columns')
    ], 
    [
        Input('submit-button-state', 'n_clicks'),
        State('index-dropdown', 'value'),
        State('columns-dropdown', 'value'),
        State('values-dropdown', 'value'),
    ])
def update_cols(n_clicks, index_val, columns_val, values_val):
    if index_val == columns_val or index_val == values_val or values_val == columns_val:
        print("Inputs must all be different!")
        return None, None
    temp = df.pivot_table(
        index=index_val,
        columns=columns_val, 
        values=values_val,
        aggfunc=identity,
    )
    out_df = pd.DataFrame(temp.to_records())
    out_cols = [{"name": i, "id": i} for i in out_df]
    return out_df.to_dict('records'), out_cols

if __name__ == '__main__':
    app.run_server(debug=True)