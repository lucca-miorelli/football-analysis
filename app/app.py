from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output
# from app.server import app
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from football_analysis.statsbomb.analysis import PassAnalysis
from football_analysis.config.constant import BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24
from pitch_plot import create_pitch

app = Dash(__name__, title='Football Analysis', update_title=None)
server = app.server

available_game_ids = BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24

default_layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=1200,
        height=800,
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
    [Output('pass-network-graph', 'figure'),
     Output('player-dropdown', 'options')],
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
    Output('player-id-output', 'children'),
    [Input('player-dropdown', 'value')]
)
def update_player_id(selected_player_id):
    return f'Player ID: {selected_player_id}'


app.layout = html.Div(children=[
    html.H1(children='Football Analysis', style={'textAlign': 'center', 'color': '#808080'}),
    html.Div(children='Visualizing Pass Networks', style={'textAlign': 'center', 'color': '#808080'}),
    dcc.Graph(
        id='pass-network-graph',
        figure={
            'data': traces,
            'layout': default_layout
        },
        config={'displayModeBar': False}
    ),
    html.Div(children=[
        html.Div(children=[
            html.H3(children='Game ID', style={'color': '#808080'}),
            dcc.Dropdown(
                id='game-dropdown',
                options=[{'label': game_id, 'value': game_id} for game_id in available_game_ids],
                value=available_game_ids[0]
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        # Add the player-dropdown here
        html.Div(children=[
            html.H3(children='Player ID', style={'color': '#808080'}),
            dcc.Dropdown(
                id='player-dropdown',
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div(id='player-id-output', style={'color': '#808080'}),
    ]),
], style={'backgroundColor': 'rgba(20, 20, 20, 0.9)'})

if __name__ == '__main__':
    app.run_server(debug=True)
