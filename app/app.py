"""Bayern Leverkusen 2023/24 Bundesliga Analysis Dashboard."""
from dash import dcc, html
import plotly.graph_objs as go
from dash import Dash
from dash.dependencies import Input, Output
from pitch_plot import create_pitch
import math

from football_analysis.config.constant import (
    GAME_ID_TITLE,
)
from football_analysis.statsbomb.analysis import Event, PassAnalysis, ShotAnalysis, MatchInfo


app = Dash(
    __name__, title="Leverkusen 23-24 Statsbomb Data", update_title=None
)
server = app.server

default_layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=800,
        height=533.33,
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        margin=dict(t=40, b=40, l=40, r=40),
    )


def create_pass_analysis(game_id):
    """Create a PassAnalysis object for the given game_id."""
    pass_analysis = PassAnalysis(
        game_id=game_id,
        team_id=904,
        starting_players_only=True
    )
    return pass_analysis

def create_shot_analysis(game_id):
    """Create a ShotAnalysis object for the given game_id."""
    shot_analysis = ShotAnalysis(
        game_id=game_id,
        team_id=904,
    )
    return shot_analysis

def create_event_analysis(game_id, player_id):
    """Create an Event object for the given game_id and player_id."""
    event_analysis = Event(
        game_id=game_id,
        player_id=player_id
    )
    return event_analysis


@app.callback(
    [Output("pass-network-graph", "figure"), Output("player-dropdown", "options")],
    [Input("game-dropdown", "value")]
)
def update_pass_analysis(game_id):
    """Update the pass network graph and player dropdown options."""
    pass_analysis = create_pass_analysis(game_id)
    temp_passes_between, temp_passers_avg_location = pass_analysis.plotly_test_network()
    title_text = f"{pass_analysis.team_name} vs {pass_analysis.opp_team_name}"

    resize_factor = 0.58

    # Update traces with new pass_analysis object
    traces = create_pitch(resize_factor=resize_factor)
    for i in range(len(temp_passes_between)):
        traces.append(
            go.Scatter(
                x=temp_passes_between[["x", "x_end"]].iloc[i].values*resize_factor,
                y=temp_passes_between[["y", "y_end"]].iloc[i].values*resize_factor,
                mode="lines",
                line={
                    "width": float(temp_passes_between["width"].iloc[i])*resize_factor,
                    "color": "rgba(128, 128, 128, 0.65)"
                },
                hovertemplate="Number of passes: %{text}",
                text=f'{temp_passes_between["pass_count"].iloc[i]}'
            )
        )
    # Add the marker trace
    traces.append(
        go.Scatter(
            x=temp_passers_avg_location["x"]*resize_factor,
            y=temp_passers_avg_location["y"]*resize_factor,
            mode="markers",
            marker={
                "size":temp_passers_avg_location["normalized_marker_size"]*resize_factor,
                "sizemode":"diameter",
                "sizemin":4*resize_factor,
                "sizeref":1/30*resize_factor,
                "color":"#E32221",
                "opacity":1,
                "line":{
                    "color": "#E32221",
                    "width": 10*resize_factor
                }
            },
            text=temp_passers_avg_location["player_name"] + " (" +
                temp_passers_avg_location["jersey_number"].astype(str) + ") - " +
                temp_passers_avg_location["position_name"] + "<br>" +
                temp_passers_avg_location["passes_given"].astype(str) +
                " passes given<br>" +
                temp_passers_avg_location["passes_received"].astype(str) +
                " passes received",
            textposition="middle center",
            hovertemplate="%{text}<extra></extra>",
            hoverinfo="text"
        )
    )

    # Update layout with new pass_analysis object
    annotations = []
    for _, row in temp_passers_avg_location.iterrows():
        annotations.append({
            "x":row["x"]*resize_factor,
            "y":row["y"]*resize_factor,
            "text":str(row["jersey_number"]),
            "showarrow":False,
            "font":{
                "size":(15*row["normalized_marker_size"]+8)*resize_factor,
                "color":"white",
                "family":"DIN Alternate, bold"
            },
            "xanchor":"center",
            "yanchor":"middle"
        })

    layout = go.Layout(
        title={
            "text": title_text,
            "font": {
                "color": "#808080",
                "size": 36*resize_factor,  # adjust as needed
                "family":"DIN Alternate, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200*resize_factor,
        height=800*resize_factor,
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[value*resize_factor for value in[0, 120]]
        },
        yaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[value*resize_factor for value in [0, 80]]
        },
        annotations=annotations,
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        margin=dict(t=40, b=40, l=40, r=40),
    )

    # Update player dropdown options
    player_dropdown_options = [
        {
            "label": f"{player[0]} ({player[2]}) | {player[3]}",
            "value": player[1]
        }
        for player
        in pass_analysis.players_df[
            ["player_name", "player_id", "position_abbreviation", "jersey_number"]
        ].values
    ]

    return {"data": traces, "layout": layout}, player_dropdown_options


@app.callback(
    Output("player-passes-graph", "figure"),
    [
        Input("game-dropdown", "value"),
        Input("player-dropdown", "value")
    ]
)
def update_player_passes(game_id, player_id=None):
    """Update the player passes graph."""
    pass_analysis = create_pass_analysis(game_id)
    # player_passes = pass_analysis.get_player_passes(int(player_id))
    player_passes = pass_analysis.team_passes

    resize_factor = 0.58

    # If player_id is not None, filter passes by player_id
    if player_id:
        player_passes = [
            pass_obj for pass_obj in player_passes
            if pass_obj["player"]["id"] == int(player_id)
        ]
    else: # If player_id is None, show first 100 passes
        player_passes = player_passes[:100]

    player_dict = pass_analysis.players_df.set_index("player_id")["player_name"].to_dict()  # noqa: E501
    title_text = "First 100 passes of the game" if player_id is None else f"Passes by {player_dict[str(player_id)]}" # noqa: E501

    annotations = []

    traces = create_pitch(resize_factor=resize_factor)
    for pass_obj in player_passes:

        start_location = pass_obj["location"]
        end_location = pass_obj["pass"]["end_location"]


        # If 'recipient' key exists, consider pass complete
        if pass_obj.get('pass', {}).get('outcome', {}).get('name', '') == "Incomplete" or "recipient" not in pass_obj["pass"]:
            # draw red arrow for incomplete passes
            arrow_color = "rgba(255, 0, 0, 0.65)"
        else:
            arrow_color = "rgba(128, 128, 128, 1)"

        # Get recipient name if exists
        recipient_name = pass_obj["pass"].get("recipient", {}).get("name", "No recipient")  # noqa: E501
        # Get body part if exists
        body_part = pass_obj["pass"].get("body_part", {}).get("name", "No body part")
        # Get outcome name if exists
        outcome_name = pass_obj["pass"].get("outcome", {}).get("name", "Complete")
        # Get player name
        player_name = pass_obj["player"]["name"]

        # Draw the shaft of the arrow as a line without hover text:
        traces.append(
            go.Scatter(
                x=[value*resize_factor for value in [start_location[0], end_location[0]]],
                y=[value*resize_factor for value in [start_location[1], end_location[1]]],
                mode="lines",
                line={"width":2*resize_factor, "color":arrow_color},
                hoverinfo="none"  # Disable hover for the lines
            )
        )
        # Create individual points for pass start and end with hover text:
        text_str = f"{player_name}<br><br>Play pattern: " + \
        f"{pass_obj['play_pattern']['name']}<br>Recipient: {recipient_name}<br>" + \
        f"Body Part: {body_part}<br>Outcome: {outcome_name}"

        traces.append(
            go.Scatter(
                x=[value*resize_factor for value in [start_location[0], end_location[0]]],
                y=[value*resize_factor for value in [start_location[1], end_location[1]]],
                mode="markers",
                marker={"size": 5*resize_factor, "color":"rgba(128, 128, 128, 0.0)"},
                text=[text_str, text_str],
                hovertemplate="%{text}<extra></extra>"
            )
        )
        # Add an arrow annotation for the pass:
        annotations.append(
            {
                "y":end_location[1]*resize_factor,
                "x":end_location[0]*resize_factor,
                "ay":start_location[1]*resize_factor,
                "ax":start_location[0]*resize_factor,
                "xref":"x",
                "yref":"y",
                "axref":"x",
                "ayref":"y",
                "showarrow":True,
                "arrowhead":1,
                "arrowsize":1,
                "arrowwidth":2,
                "arrowcolor":arrow_color
            }
        )
    layout = go.Layout(
        title={
            "text": title_text,
            "font": {
                "color": "#808080",
                "size": 36*resize_factor,  # adjust as needed
                "family":"DIN Alternate, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200*resize_factor, # 1200, 800, 600
        height=800*resize_factor, # 800, 533.33, 400
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[value*resize_factor for value in [0, 120]]
        },
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "range": [value*resize_factor for value in [0, 80]]
        },
        plot_bgcolor="rgba(20, 20, 20, 0.0)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        annotations=annotations,
        margin=dict(t=40, b=40, l=40, r=40),
    )

    return {"data": traces, "layout": layout}


@app.callback(
    Output("shots-graph", "figure"),
    [
        Input("game-dropdown", "value"),
        Input("player-dropdown", "value")
    ]
)
def update_shot_chart(game_id, player_id=None):
    """Update the shots graph."""
    shot_analysis = create_shot_analysis(game_id)
    player_shots = shot_analysis.team_shots

    # If player_id is not None, filter shots by player_id
    if player_id:
        player_shots = [
            shot for shot in player_shots if shot["player"]["id"] == int(player_id)
        ]
    else:
        player_shots = player_shots[:100]

    annotations = []
    resize_factor = 0.58

    traces = create_pitch(resize_factor=resize_factor)
    for shot_obj in player_shots:

        start_location = shot_obj["location"]
        end_location = shot_obj["shot"]["end_location"]


        # If outcome is Goal, set color to green
        if shot_obj["shot"]["outcome"]["name"] == "Goal":
            marker_color = "rgba(0, 255, 0, 0.65)"
        else:
            # draw red arrow for missed shots
            marker_color = "rgba(255, 0, 0, 0.50)"

        # Get technique name if exists
        technique_name = shot_obj["shot"].get("technique", {}).get("name", "No technique")  # noqa: E501
        # Get body part if exists
        body_part = shot_obj["shot"].get("body_part", {}).get("name", "No body part")
        # Get outcome name if exists
        outcome_name = shot_obj["shot"].get("outcome", {}).get("name", "Complete")
        # Get type name if exists
        type_name = shot_obj["shot"].get("type", {}).get("name", "No type")
        # Get player name
        player_name = shot_obj["player"]["name"]
        # Get statsbomb_xg
        statsbomb_xg = shot_obj["shot"].get("statsbomb_xg", "No xG")
        # Adjust marker size based on logarithmic scale
        marker_size = math.log(statsbomb_xg + 1) * 100


        # Draw the shaft of the arrow as a line without hover text:
        traces.append(
            go.Scatter(
                x=[value*resize_factor for value in [start_location[0]]],
                y=[value*resize_factor for value in [start_location[1]]],
                mode="markers",
                line={
                    "width":4*resize_factor,
                    "color":marker_color
                },
                hoverinfo="none"  # Disable hover for the lines
            )
        )
        # Create individual points for pass start and end with hover text:
        text_str = f"{player_name} (xG: {statsbomb_xg:.2f})<br><br>Play pattern: " + \
        f"{shot_obj['play_pattern']['name']}<br>Recipient: {type_name}<br>Body Part: " + \
        f"{body_part}<br>Outcome: {outcome_name}<br>Technique: {technique_name}"

        traces.append(
            go.Scatter(
                x=[value*resize_factor for value in [start_location[0]]],
                y=[value*resize_factor for value in [start_location[1]]],
                mode="markers",
                marker={"size":1*resize_factor, "color": "rgba(128, 128, 128, 0.0)"},
                # marker={
                #     "size":marker_size,
                #     "sizemode":"diameter",
                #     "sizeref":1,
                #     "color":marker_color,
                #     "opacity":0.65
                # },
                text=[text_str, text_str],
                hovertemplate="%{text}<extra></extra>"
            )
        )
        # Add an arrow annotation for the pass:
        annotations.append({
                "y":end_location[1]*resize_factor,
                "x":end_location[0]*resize_factor,
                "ay":start_location[1]*resize_factor,
                "ax":start_location[0]*resize_factor,
                "xref":"x",
                "yref":"y",
                "axref":"x",
                "ayref":"y",
                "showarrow":True,
                "arrowhead":1,
                "arrowsize":1,
                "arrowwidth":2,
                "arrowcolor":marker_color
        })
    layout = go.Layout(
        title={
            "text": "Shots by Team",
            "font": {
                "color": "#808080",
                "size": 36*resize_factor,  # adjust as needed
                "family":"DIN Alternate, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200*resize_factor,
        height=800*resize_factor,
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[value*resize_factor for value in [0, 120]]
        },
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "range":[value*resize_factor for value in[0, 80]]
        },
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        annotations=annotations,  # Include the annotations here
        margin=dict(t=40, b=40, l=40, r=40),
    )

    return {"data": traces, "layout": layout}


@app.callback(
        Output("radar-chart", "figure"),
        [
            Input("game-dropdown", "value"),
            Input("player-dropdown", "value")
        ]
)
def update_radar_chart(game_id, player_id=None):
    """Update the radar chart."""
    event_analysis = create_event_analysis(game_id, player_id)
    event_count = event_analysis.event_count
    # opp_event_count = event_analysis.opp_event_count

    data = [
        go.Scatterpolar(
            r=list(event_count.values()),
            theta=list(event_count.keys()),
            fill="toself",
            name="Player Events",
            fillcolor="rgba(255, 0, 0, 0.65)",
            line={"color":"rgba(255, 0, 0, 0.65)"}
        ),
        # go.Scatterpolar(
        #     r=list(opp_event_count.values()),
        #     theta=list(opp_event_count.keys()),
        #     fill='toself',
        #     name='Opponent Events',
        #     fillcolor='rgba(128, 128, 128, 0.65)',
        #     line=dict(color='rgba(128, 128, 128, 0.65)')
        # )
    ]

    layout = go.Layout(
        polar={
            "bgcolor":"rgba(20, 20, 20, 0.9)",
            "radialaxis":{
                "showgrid":True,
                "gridcolor":"rgba(128, 128, 128, 0.3)"
            },
            "angularaxis": {
                "showgrid":True,
                "gridcolor":"rgba(128, 128, 128, 0.5)",
                "linecolor":"rgba(128, 128, 128, 0.5)",
                "tickfont":{
                    "color":"rgba(128, 128, 128, 1)",
                    "size": 10,
                    "family":"DIN Alternate, bold"
                },
                # "tickangle": -45  # rotate labels
            }
        },
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        width=600,
        height=533.33,
        margin=dict(t=40, b=40, l=80, r=80),  # increase left and right margins
    )

    return {"data": data, "layout": layout}

@app.callback(
    Output("shot-bubble-graph", "figure"),
    [
        Input("game-dropdown", "value"),
        Input("player-dropdown", "value")
    ]
)
def update_shot_bubble_chart(game_id, player_id=None):
    """Update the shot bubble chart."""
    shot_analysis = create_shot_analysis(game_id)
    player_shots = shot_analysis.team_shots

    # If player_id is not None, filter shots by player_id
    if player_id:
        player_shots = [
            shot for shot in player_shots if shot["player"]["id"] == int(player_id)
        ]

    resize_factor = 0.58

    traces = create_pitch(resize_factor=resize_factor)
    for shot_obj in player_shots:

        start_location = shot_obj["location"]
        # end_location = shot_obj["shot"]["end_location"]

        # If outcome is Goal, set color to green
        if shot_obj["shot"]["outcome"]["name"] == "Goal":
            marker_color = "rgba(0, 255, 0, 0.65)"
        else:
            # draw red arrow for missed shots
            marker_color = "rgba(255, 0, 0, 0.50)"

        # Get technique name if exists
        technique_name = shot_obj["shot"].get("technique", {}).get("name", "No technique")
        # Get body part if exists
        body_part = shot_obj["shot"].get("body_part", {}).get("name", "No body part")
        # Get outcome name if exists
        outcome_name = shot_obj["shot"].get("outcome", {}).get("name", "Complete")
        # Get type name if exists
        type_name = shot_obj["shot"].get("type", {}).get("name", "No type")
        # Get player name
        player_name = shot_obj["player"]["name"]
        # Get statsbomb_xg
        statsbomb_xg = shot_obj["shot"].get("statsbomb_xg", "No xG")
        # Adjust marker size based on logarithmic scale
        marker_size = math.log(statsbomb_xg + 1) * 100

        text_str = f"{player_name} (xG: {statsbomb_xg:.2f})<br><br>Play pattern: " + \
                f"{shot_obj['play_pattern']['name']}<br>Recipient: {type_name}<br>Body Part: " + \
                f"{body_part}<br>Outcome: {outcome_name}<br>Technique: {technique_name}"

        traces.append(
            go.Scatter(
                x=[start_location[0]*resize_factor],
                y=[start_location[1]*resize_factor],
                mode="markers",
                marker={
                    "size":marker_size,
                    "sizemode":"diameter",
                    "sizeref":1,
                    "color":marker_color,
                    "opacity":0.65
                },
                text=[text_str],
                hovertemplate="%{text}<extra></extra>"
            )
        )

    layout = go.Layout(
        title={
            "text": "Shots by Team",
            "font": {
                "color": "#808080",
                "size": 36*resize_factor,  # adjust as needed
                "family":"DIN Alternate, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200*resize_factor,
        height=800*resize_factor,
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[value*resize_factor for value in [0, 120]]
        },
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "range":[value*resize_factor for value in[0, 80]]
        },
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        # annotations=annotations,  # Include the annotations here
        margin=dict(t=40, b=40, l=40, r=40),
    )
    return {"data": traces, "layout": layout}

@ app.callback(
    Output("match-info", "children"),
    [Input("game-dropdown", "value")]
)
def update_match_info(game_id=None):
    """Update the match info."""
    if game_id:
        match = MatchInfo(game_id=game_id)

        home_team = match.match_info.get("home_team", {}).get("home_team_name", "Home Team")
        away_team = match.match_info.get("away_team", {}).get("away_team_name", "Away Team")
        home_score = match.match_info.get("home_score", 0)
        away_score = match.match_info.get("away_score", 0)

        match_scoreboard = f"{home_team} {home_score} x {away_score} {away_team}"
    else:
        match_scoreboard = "No match info available"

    return match_scoreboard


app.layout = html.Div(children=[
    html.Div(className="header-section", style={'textAlign': 'center'}, children=[
        html.Img(
            src=app.get_asset_url("../assets/figures/bayer_leverkusen.png"),
            style={
                "width":"120px",
                "height":"90px",
            }
        ),
        html.H1(
            children="Bayer Leverkusen 2023/24 Bundesliga Analysis",
            className="center-text"),
        html.Img(
            src=app.get_asset_url("../assets/figures/sb_logo_colour.png"),
            style={
                "width":"240px",
                "height":"38px",
            }
        )
    ]),

    html.Div(className="dropdown-section", children=[
        html.Div(children=[
            html.H3(children="Game ID", style={"color": "#808080"}),
            dcc.Dropdown(
                id="game-dropdown",
                options=[
                    {"label": game[1], "value": game[0]}
                    for game in GAME_ID_TITLE.items()
                ],
                value=list(GAME_ID_TITLE.items())[0][0]
            )
        ], style={"width": "45%"}),

        html.Div(children=[
            html.H3(children="Player ID", style={"color": "#808080"}),
            dcc.Dropdown(
                id="player-dropdown",
            )
        ], style={"width": "45%"}),

        # html.Div(id='player-id-output', style={'color': '#808080'}),
    ]),
    html.Div(id="match-info-div", children=[
        html.H2(id="match-info", style={"textAlign": "center", "color": "#808080"}),
    ], style={"textAlign": "center", "color": "#808080"}
    ),
    html.Div(className="pitch-graphs-section", children=[
        html.Div(id="pass-network-container", children=[
            dcc.Graph(
                id="pass-network-graph",
                figure={
                    "data": [],
                    "layout": default_layout
                },
                config={"displayModeBar": False},
                # style={
                #     'flexBasis': '50%',
                #     'width': '50%',
                #     'margin': 'auto'  # Center and align horizontally
                # }
            )
        ]),
        html.Div(id="radar-chart-container", children=[
            dcc.Graph(
                id="radar-chart",
                figure={
                    "data": [],
                    "layout": default_layout
                },
                config={"displayModeBar": False},
                # style={
                #     'flexBasis': '50%',
                #     'width': '50%',
                #     'margin': 'auto'  # Center and align horizontally
                # }
            ),
        ]),
    ]),
    html.Div(className="passes-and-shots-section", children=[
        html.Div(className="player-passes-section", children=[
            dcc.Graph(
                id="player-passes-graph",
                figure={
                    "data": [],
                    "layout": default_layout
                },
                config={"displayModeBar": False},
                # style={
                #     'flexBasis': '50%',
                #     'width': '50vw',
                #     'height': '100vh',  # Adjust the height as needed
                #     'margin': 'auto'  # Center and align horizontally
                # }
            ),
        ]),
        html.Div(className="shots-section", children=[
            dcc.Graph(
                id="shots-graph",
                figure={
                    "data": [],
                    "layout": default_layout
                },
                config={"displayModeBar": False},
                # style={
                #     'flexBasis': '50%',
                #     'width': '50vw',
                #     'height': '100vh',  # Adjust the height as needed
                #     'margin': 'auto'  # Center and align horizontally
                # }
            ),
        ]),
    ]),
    html.Div(className="shots-bubble-section", children=[
        html.Div(className="shots-bubble-chart", children=[
            dcc.Graph(
                id="shot-bubble-graph",
                figure={
                    "data": [],
                    "layout": default_layout
                },
                config={"displayModeBar": False},
                # style={
                #     'margin': 'auto'  # Center and align horizontally
                # }
            )
        ]),
    ]),
], style={"backgroundColor": "rgba(20, 20, 20, 0.9)"})



if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8060)
