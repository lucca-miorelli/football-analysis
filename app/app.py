# from app.server import app
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, Input, Output, dcc, html
from dash.dependencies import Input, Output
from pitch_plot import create_pitch, create_half_pitch_rotated

from football_analysis.config.constant import (
    BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24, GAME_ID_TITLE)
from football_analysis.statsbomb.analysis import PassAnalysis

app = Dash(__name__, title='Leverkusen 23-24 Statsbomb Data', update_title=None)
server = app.server

available_game_ids = BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24

default_layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=800,
        height=533.33,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(20, 20, 20, 0.9)',
        paper_bgcolor='rgba(20, 20, 20, 0.9)'
    )


def create_pass_analysis(game_id):
    pass_analysis = PassAnalysis(
        game_id=game_id,
        team_id=904,
        starting_players_only=True
    )
    return pass_analysis

traces = create_pitch()

@app.callback(
    [
        Output('pass-network-graph', 'figure'),
        Output('player-dropdown', 'options')
    ],
    [Input('game-dropdown', 'value')]
)
def update_pass_analysis(game_id):
    pass_analysis = create_pass_analysis(game_id)
    temp_passes_between, temp_passers_avg_location, color = pass_analysis.plotly_test_network()
    title_text = f"{pass_analysis.team_name} vs {pass_analysis.opp_team_name}"


    # Update traces with new pass_analysis object
    traces = create_pitch()
    for i in range(len(temp_passes_between)):
        traces.append(
            go.Scatter(
                x=temp_passes_between[['x', 'x_end']].iloc[i].values,
                y=temp_passes_between[['y', 'y_end']].iloc[i].values,
                mode='lines',
                line=dict(width=float(temp_passes_between['width'].iloc[i]), color='rgba(128, 128, 128, 0.75)'),
                hovertemplate='Number of passes: %{text}',
                text=f'{temp_passes_between["pass_count"].iloc[i]}'
            )
        )
    # Add the marker trace
    traces.append(
        go.Scatter(
            x=temp_passers_avg_location['x'],
            y=temp_passers_avg_location['y'],
            mode='markers',
            marker=dict(
                size=temp_passers_avg_location['normalized_marker_size'],  # Replace 'your_column' with the name of your column
                sizemode='diameter',  # Marker size is set by diameter
                sizemin=4,  # Minimum marker size
                sizeref=1/30,  # Adjust this value to change the scaling of your marker sizes
                color='#E32221',
                opacity=1,  # Ensure markers are completely opaque
                line=dict(color= "#E32221",width=10)
            ),
            text=temp_passers_avg_location['player_name'] + ' (' +
                temp_passers_avg_location['jersey_number'].astype(str) + ') - ' +
                temp_passers_avg_location['position_name'] + '<br>' + 
                temp_passers_avg_location['passes_given'].astype(str) + ' passes given<br>' + 
                temp_passers_avg_location['passes_received'].astype(str) + ' passes received',
            textposition='middle center',
            hovertemplate='%{text}<extra></extra>', # Only display the text when hovering
            hoverinfo='text' # Disable default hover info
        )
    )

    # Update layout with new pass_analysis object
    annotations = []
    for i, row in temp_passers_avg_location.iterrows():
        annotations.append(dict(
            x=row['x'],
            y=row['y'],
            text=str(row['jersey_number']),
            showarrow=False,
            font=dict(size=15*row['normalized_marker_size']+8, color='white', family="Arial, bold"),
            xanchor='center',
            yanchor='middle'
        ))

    layout = go.Layout(
        title={
            'text': title_text,
            'font': {
                'color': '#808080',
                'size': 24,  # adjust as needed
                'family': 'Arial, bold'
            },
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        autosize=False,
        width=1200,
        height=800,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 120]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 80]),
        annotations=annotations,
        plot_bgcolor='rgba(20, 20, 20, 0.9)',
        paper_bgcolor='rgba(20, 20, 20, 0.9)'
    )

    # Update player dropdown options
    player_dropdown_options = [{'label': player[0], 'value': player[1]} for player in pass_analysis.players_df[['player_name', 'player_id']].values]

    return {'data': traces, 'layout': layout}, player_dropdown_options


@app.callback(
    Output('vertical-passes-graph', 'figure'),
    [
        Input('game-dropdown', 'value'),
        Input('player-dropdown', 'value')
    ]
)
def update_vertical_passes(game_id, player_id):
    print("############ HERE ############")
    print(game_id, player_id)
    print("############ player_id type ############")
    print(type(player_id))
    pass_analysis = create_pass_analysis(game_id)
    player_passes = pass_analysis.get_player_passes(int(player_id))
    print("TYPE")
    print(type(player_passes))
    print("LEN")
    print(len(player_passes))
    print("PLAYER PASSES")
    print(player_passes)
    # player_passes = player_passes[player_passes['pass_height_name'] == 'Ground']

    player_dict = pass_analysis.players_df.set_index('player_id')["player_name"].to_dict()

    annotations = []

    traces = create_half_pitch_rotated()
    for pass_obj in player_passes:
        # Draw the shaft of the arrow as a line without hover text:
        traces.append(
            go.Scatter(
                x=[(pass_obj["location"][1]-80)*(-1), (pass_obj["pass"]["end_location"][1]-80)*(-1)],
                y=[pass_obj["location"][0]-60, pass_obj["pass"]["end_location"][0]-60],
                mode='lines',
                line=dict(width=2, color='rgba(128, 128, 128, 0.75)'),
                hoverinfo='none'  # Disable hover for the lines
            )
        )
        # Create individual points for pass start and end with hover text:
        traces.append(
            go.Scatter(
                x=[(pass_obj["location"][1]-80)*(-1), (pass_obj["pass"]["end_location"][1]-80)*(-1)],
                y=[pass_obj["location"][0]-60, pass_obj["pass"]["end_location"][0]-60],
                mode='markers',
                marker=dict(size=5, color='rgba(128, 128, 128, 0.75)'),
                text=[pass_obj["play_pattern"]["name"], pass_obj["play_pattern"]["name"]],
                hovertemplate="%{text}<extra></extra>"
            )
        )
        # Add an arrow annotation for the pass:
        annotations.append(
            dict(
                x=(pass_obj["pass"]["end_location"][1]-80)*(-1),
                y=pass_obj["pass"]["end_location"][0]-60,
                ax=(pass_obj["location"][1]-80)*(-1),
                ay=pass_obj["location"][0]-60,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=1,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='rgba(128, 128, 128, 0.75)'
            )
        )
    layout = go.Layout(
        title={
            'text': f'Vertical Passes by {player_dict[str(player_id)]}',
            'font': {
                'color': '#808080',
                'size': 24,  # adjust as needed
                'family': 'Arial, bold'
            },
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        autosize=False,
        width=1200,
        height=800,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 120]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 80]),
        plot_bgcolor='rgba(20, 20, 20, 0.9)',
        paper_bgcolor='rgba(20, 20, 20, 0.9)',
        annotations=annotations  # Include the annotations here
    )

    return {'data': traces, 'layout': layout}



@app.callback(
    Output('player-id-output', 'children'),
    [Input('player-dropdown', 'value')]
)
def update_player_id(selected_player_id):
    return f'Player ID: {selected_player_id}'


app.layout = html.Div(children=[
    html.Div(className='header-section', children=[
        html.Img(
            src=app.get_asset_url('../assets/figures/bayer_leverkusen.png'),
            style=dict(
                width='120px',
                height='90px',
            )
        ),
        html.H1(children='Bayer Leverkusen 2023/24 Bundesliga Analysis', className='center-text'),
        html.Img(
            src=app.get_asset_url('../assets/figures/sb_logo_colour.png'),
            style=dict(
                width='240px',
                height='38px',
            )
        )
    ]),
    
    html.Div(className='dropdown-section', children=[
        html.Div(children=[
            html.H3(children='Game ID', style={'color': '#808080'}),
            dcc.Dropdown(
                id='game-dropdown',
                options=[{'label': game[1], 'value': game[0]} for game in GAME_ID_TITLE.items()],
                value=available_game_ids[0]
            )
        ], style={'width': '45%'}),
        
        html.Div(children=[
            html.H3(children='Player ID', style={'color': '#808080'}),
            dcc.Dropdown(
                id='player-dropdown',
            )
        ], style={'width': '45%'}),
        
        html.Div(id='player-id-output', style={'color': '#808080'}),
    ]),
    html.Div(className='pitch-graphs-section', children=[
    
        html.Div(className='pass-network-section', children=[
            dcc.Graph(
                id='pass-network-graph',
                figure={
                    'data': traces,
                    'layout': default_layout
                },
                config={'displayModeBar': False}
            ),
        ]),
        html.Div(className='vertical-passes-section', children=[
            dcc.Graph(
                id='vertical-passes-graph',
                figure={
                    'data': [],
                    'layout': default_layout
                },
                config={'displayModeBar': False}
            ),
        ]),
    ]),

], style={'backgroundColor': 'rgba(20, 20, 20, 0.9)'})




if __name__ == '__main__':
    app.run_server(debug=True)
