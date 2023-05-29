# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import csv

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
#spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                options=[{'label':'All Site','value':'ALL'}, 
                                         {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                         {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                         {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                         {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                 value='ALL',
                                 placeholder="Select a Launch Site",
                                 searchable=True
                                 ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=spacex_df['Payload Mass (kg)'].min(),
                                                max=spacex_df['Payload Mass (kg)'].max(), step=1000, marks=500, 
                                                value=[spacex_df['Payload Mass (kg)'].min(),
                                                       spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([], id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback([Output(component_id='success-pie-chart', component_property='children'),
               Output(component_id='success-payload-scatter-chart', component_property='children')],
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_pie_chart(entered_site, slider):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(data_frame=spacex_df, values='Flight Number',
        names='Launch Site',
        title='Total Successes by Location')
        
        load_df = spacex_df[spacex_df['Payload Mass (kg)'].between(slider[0], slider[1])]
        load = px.scatter(data_frame=load_df, x='Launch Site', y='Payload Mass (kg)', facet_col='class')

        return([dcc.Graph(figure=fig),
                dcc.Graph(figure=load)])
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(data_frame=filtered_df, values='Flight Number', names='class',
        title='Successes for ' + entered_site)

        load_df = filtered_df[filtered_df['Payload Mass (kg)'].between(slider[0], slider[1])]
        load = px.scatter(data_frame=load_df, x='Launch Site', y='Payload Mass (kg)', facet_col='class')

        return([dcc.Graph(figure=fig),
                dcc.Graph(figure=load)])

px.box()

# Run the app
if __name__ == '__main__':
    app.run_server()
