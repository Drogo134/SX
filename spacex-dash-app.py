# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# 1. Read the data and prepare initial variables
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Prepare the list of options for the dropdown
launch_sites = spacex_df['Launch Site'].unique().tolist()
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    site_options.append({'label': site, 'value': site})

# 2. Create the Dash application instance
app = dash.Dash(__name__)

# 3. Define the application's layout (the visual structure)
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # TASK 1: Add the Dropdown component
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # Placeholder for the Pie Chart (will be populated by TASK 2 callback)
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add the Range Slider component
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # Placeholder for the Scatter Plot (will be populated by TASK 4 callback)
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# 4. Define the application's callbacks (the interactive logic)

# TASK 2: Callback to update the Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Pie chart for all sites
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches By Site',
            hole=0.3  # Optional: Add a donut effect
        )
        return fig
    else:
        # Pie chart for a specific site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['Outcome', 'Count']
        fig = px.pie(
            success_counts,
            values='Count',
            names='Outcome',
            title=f'Total Success Launches for Site {entered_site}',
            hole=0.3  # Optional: Add a donut effect
        )
        return fig

# TASK 4: Callback to update the Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    
    if entered_site == 'ALL':
        # Scatter plot for all sites
        filtered_df = spacex_df[mask]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites',
            labels={'class': 'Class'}
        )
        return fig
    else:
        # Scatter plot for a specific site
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & mask]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for Site {entered_site}',
            labels={'class': 'Class'}
        )
        return fig

# 5. Run the application
if __name__ == '__main__':
    app.run(debug=True)