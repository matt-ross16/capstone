# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#print(spacex_df.head())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site Here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload],
                                    marks={
                                        0:'0 kg',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(drop_select):
    if drop_select == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == drop_select]
        pie_data = filtered_df.groupby(["Launch Site", 'class']).size().reset_index()
        pie_data = pie_data.rename(columns={0:'class count'})
        fig = px.pie(pie_data, values='class count', names='class', title='Total Success Launches for site ' + drop_select)
    
    fig.update_layout(transition_duration=500)

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')]
)
def update_scatter(drop_select, slider_value):
    low, high = slider_value
    masks = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    df_scatter = spacex_df[masks]

    if drop_select == 'ALL':
        fig = px.scatter(
            df_scatter,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = df_scatter[df_scatter["Launch Site"] == drop_select]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for Site ' + drop_select)

    fig.update_layout(transition_duration=500)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()