import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import analysis
import base64

# Spotipy Setup
cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
secret = 'a761b0fa42734f5aa5a4182f425558c6'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

external_stylesheet = [
    {
        "href": 'assets/typography.css',
        "rel": 'stylesheet'
    }
]

# imports picture and reads in base 64 code
image_filename = 'clef2.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# define features and initialize their value
init_taste = ['danceability', 'acousticness', 'energy', 'instrumentalness',
              'speechiness', 'liveness', 'valence']
init_scale = [0, 0, 0, 0, 0, 0, 0, 0]
# create the initial stargraph
fig = analysis.star_graph(init_taste, init_scale)

# create popular graph
popular_taste, popular_scale = analysis.generate_general_taste('US')
fig2 = analysis.star_graph(popular_taste, popular_scale)

# Background and color scheme pre-coded colors
colors = {
    'background': '#333333',
    'text': '#7FDBFF'
}

# Run Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Br(),
                html.P(children=html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image.decode())),
                    className="header-emoji",
                    style={"textAlign": 'center',
                           'backgroundColor': colors['background'],
                           'height': '54px'}),
                html.H1(children='Music Investigator',
                        style={'textAlign': 'center',
                               'color': '#A01FF2',
                               'backgroundColor': colors['background']
                               },
                        ),
                html.Div('Web Dashboard for Data Visualization using Python',
                         style={'textAlign': 'center',
                                'color': '#FFFFFF',
                                'backgroundColor': colors['background']}),
                html.Div('Spotify User Information',
                         style={'textAlign': 'center',
                                'color': '#FFFFFF',
                                'backgroundColor': colors['background']}),
                html.Br(),
                html.Br(),

                # This part allow us to take input
                html.Div(["ENTER YOUR SPOTIFY ACCOUNT ID: ",
                          dcc.Input(id='my-input', value='...text here...', type='text')],
                         style={'margin-bottom': '24px',
                                'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
                                'color': '#FFFFFF',
                                'textAlign': ''}),
            ], style={'height': '250px',
                      'backgroundColor': colors['background']}
        ),
        html.Br(),
        html.Hr(style={'color': '#7FDBFF'}),
        html.Div("This Graph Represents YOUR Music Taste"),
        dcc.Graph(id='graph1', figure=fig,
                  style={'margin-bottom': '24px',
                         'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
                         'color': '#FFFFFF'}),
        html.Br(),

        # This part show different countries' tastes
        html.Div("This Graph Represents the Music Taste Across Different Countries"),
        dcc.Graph(id='graph2', figure=fig2),
        html.Br(),
        html.Div('Please Select a Country',
                 style={'margin': '10px',
                        'margin-bottom': '24px',
                        'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
                        }),
        dcc.Dropdown(
            id='select-country',
            options=[
                {'label': 'United States of America', 'value': 'US'},
                {'label': 'Andorra', 'value': 'AD'},
                {'label': 'Australia', 'value': 'AU'},
                {'label': 'Brazil', 'value': 'BR'},
                {'label': 'Canada', 'value': 'CA'},
                {'label': 'Chile', 'value': 'CL'},
            ],
            value='USA'
        ),
        html.Div('*This is the conclusion*'),
    ])


@app.callback(
    Output('graph1', 'figure'),
    Input('my-input', 'value')
)
def update_graph1(input_value):
    taste, scale = analysis.generate_elements(input_value)
    fig = analysis.star_graph(taste, scale)
    return fig


@app.callback(
    Output('graph2', 'figure'),
    Input('select-country', 'value')
)
def update_graph2(country):
    taste, scale = analysis.generate_general_taste(country)
    fig = analysis.star_graph(taste, scale)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
