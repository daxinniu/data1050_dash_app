import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

from app import app, historical_data

# Connect to the layout and callbacks of each tab
from all_state_graph import all_state_graph_layout
from by_state_graph import by_state_graph_layout
from Approval import Approval_US_layout
from map import map_layout
from concern import concern_US_layout
from image import image_layout
# from trends import trends_layout
# from other import other_layout


# our app's Tabs *********************************************************
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Overview", tab_id="tab-all_state_graph", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="By State", tab_id="tab-by_state_graph", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Map", tab_id="tab-map", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Gov Admin Approval", tab_id="tab-approval", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Concern Level", tab_id="tab-concern", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="About Us", tab_id="tab-about", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-all_state_graph",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    html.Br(),
    dbc.Row(dbc.Col(html.H1("Covid Data Analysis Dashboard",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-all_state_graph":
        return all_state_graph_layout
    elif tab_chosen == "tab-by_state_graph":
        return by_state_graph_layout
    elif tab_chosen == "tab-map":
        return map_layout
    elif tab_chosen == 'tab-approval':
        return Approval_US_layout
    elif tab_chosen == 'tab-concern':
        return concern_US_layout
    elif tab_chosen == 'tab-about':
        return image_layout
    return html.P("This shouldn't be displayed for now...")



if __name__=='__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)