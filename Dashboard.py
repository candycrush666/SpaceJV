import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load the SpaceX dataset
spacex_df = pd.read_csv('C:/spacex_launch_dash.csv')

# Create a Dash application
app = dash.Dash(__name__)

# Create a list of launch sites
launch_sites = spacex_df['Launch Site'].unique()
launch_site_options = [{'label': site, 'value': site} for site in launch_sites]

# Create a list of booster versions
booster_versions = spacex_df['Booster Version'].unique()
booster_version_options = [{'label': version, 'value': version} for version in booster_versions]

# Define the layout of the Dash application
app.layout = html.Div([
    html.H1("SpaceX Launch Data Dashboard"),
    dcc.Dropdown(id='site-dropdown', options=launch_site_options, value='All Sites', placeholder="Select a Launch Site"),
    dcc.Graph(id='success-pie-chart'),
    html.Div([
        html.H2("Payload range (kg)"),
        dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[0, 10000],
                        marks={0: '0', 10000: '10000'}),
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])

# Define callback to update success pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        fig = px.pie(spacex_df, names='class', title='Total Success Launches')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Success Launches at {selected_site}')
    return fig

# Define callback to update payload scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'All Sites':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
