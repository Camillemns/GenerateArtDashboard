# Run this app with 'python dashboard.py'
# And visit http://127.0.0.1:8050/

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

artist_data = pd.read_csv('assets/archive/artists.csv')

number_of_art_by_artist = px.bar(artist_data.sort_values(by='paintings'), x='name', y='paintings', title='Number of artworks per artists')

art_by_genre = artist_data.groupby('genre').sum()

nb_of_art_by_genre = px.bar(art_by_genre.sort_values(by='paintings'), x=art_by_genre.index, y='paintings', title='Number of artworks per genre')

nb_of_artist_by_genre = px.bar(artist_data.groupby('genre').count().sort_values(by='name'), x=artist_data.groupby('genre').count().index, y='name', title='Number of artist per genre')

art_by_country = artist_data.groupby('nationality').sum()
nb_of_art_by_country = px.bar(art_by_country.sort_values(by='paintings'), x=art_by_country.index, y='paintings', title='Number of artworks per nationality')

nb_of_artist_by_country = px.bar(artist_data.groupby('nationality').count().sort_values(by='name'), x=artist_data.groupby('nationality').count().index, y='name', title='Number of artist per nationality')

image_data = {}
for artist in os.listdir('assets/archive/images/images'):
    image_data[artist] = []
    for art_img in os.listdir(f'assets/archive/images/images/{artist}'):
        image_data[artist].append(f'archive/images/images/{artist}/{art_img}')

app.layout = html.Div(children=[
    html.H1(children='Overview of the best artwork of all time'),
    html.H2(children='''
        A dashboard on art.
    '''),
    dcc.Graph(
        id='artist-plot',
        figure=number_of_art_by_artist
    ),
    dcc.Graph(
        id='genre-plot',
        figure=nb_of_art_by_genre
    ),
    dcc.Graph(
        id='genre-artist-plot',
        figure=nb_of_artist_by_genre
    ),
    dcc.Graph(
        id='nationality-plot',
        figure=nb_of_art_by_country
    ),
    dcc.Graph(
        id='nationality-artist-plot',
        figure=nb_of_artist_by_country
    ),
    html.H2(children='''
        Insight on artists :
    '''),
    dcc.Dropdown(
        id='artist-dropdown',
        options=[
            {'label': n, 'value': n} for n in artist_data.name
        ]
    ),
    html.Div(
        id='ad-output-container'
    ),
    html.H2(
        id='slider-text',
        children = 'Slide to see more art from this artist.'
    ),
    dcc.Slider(
        id='art-slider',
        min=0,
        step=1,
        value=0
    ),
    html.Div(id='slider-art'),
    html.Img(
        id='ad-output-image',
        style={
            'display': 'block',
            'margin-left': 'auto',
            'margin-right': 'auto'
        }
    )
])
@app.callback(
    dash.dependencies.Output('ad-output-container', 'children'),
    dash.dependencies.Input('artist-dropdown', 'value')
)
def update_output(value):
    return artist_data[artist_data.name == value]['bio']
'''
@app.callback(
    dash.dependencies.Output('ad-output-image', 'src'),
    dash.dependencies.Input('artist-dropdown', 'value')
)
def update_image(value):
    chosed = random_img(image_data,value.replace(' ','_'))
    return app.get_asset_url(chosed)
'''

@app.callback(
    dash.dependencies.Output('ad-output-image', 'src'),
    dash.dependencies.Output('art-slider', 'max'),
    [dash.dependencies.Input('art-slider', 'value'),
     dash.dependencies.Input('artist-dropdown', 'value')])
def update_slider_(value_slid, value_drop):
    url_list = image_data[value_drop.replace(' ', '_')]
    maxi = len(url_list)
    src = url_list[value_slid]
    return app.get_asset_url(src), maxi

'''
def random_img(url_dict, artist, id):
    url_list = url_dict[artist]
    choosen = random.randint(0, len(url_list))
    return url_list[choosen]
'''

if __name__ == '__main__':
    app.run_server(debug=True)
