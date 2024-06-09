"""Bayern Leverkusen 2023/24 Bundesliga Analysis Dashboard."""
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash import Dash
from dash.dependencies import Input, Output
from pitch_plot import create_pitch

from football_analysis.config.constant import (
    GAME_ID_TITLE,
)
from football_analysis.statsbomb.analysis import Event, PassAnalysis, ShotAnalysis

app = Dash(__name__, title="Leverkusen 23-24 Statsbomb Data", update_title=None)
server = app.server

default_layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=800,
        height=533.33,
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)"
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


    # Update traces with new pass_analysis object
    traces = create_pitch()
    for i in range(len(temp_passes_between)):
        traces.append(
            go.Scatter(
                x=temp_passes_between[["x", "x_end"]].iloc[i].values,
                y=temp_passes_between[["y", "y_end"]].iloc[i].values,
                mode="lines",
                line={
                    "width": float(temp_passes_between["width"].iloc[i]),
                    "color": "rgba(128, 128, 128, 0.75)"
                },
                hovertemplate="Number of passes: %{text}",
                text=f'{temp_passes_between["pass_count"].iloc[i]}'
            )
        )
    # Add the marker trace
    traces.append(
        go.Scatter(
            x=temp_passers_avg_location["x"],
            y=temp_passers_avg_location["y"],
            mode="markers",
            marker={
                "size":temp_passers_avg_location["normalized_marker_size"],
                "sizemode":"diameter",
                "sizemin":4,
                "sizeref":1/30,
                "color":"#E32221",
                "opacity":1,
                "line":{
                    "color": "#E32221",
                    "width": 10
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
            "x":row["x"],
            "y":row["y"],
            "text":str(row["jersey_number"]),
            "showarrow":False,
            "font":{
                "size":15*row["normalized_marker_size"]+8,
                "color":"white",
                "family":"Arial, bold"
            },
            "xanchor":"center",
            "yanchor":"middle"
        })

    layout = go.Layout(
        title={
            "text": title_text,
            "font": {
                "color": "#808080",
                "size": 24,  # adjust as needed
                "family": "Arial, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200,
        height=800,
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[0, 120]
        },
        yaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[0, 80]
        },
        annotations=annotations,
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)"
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

    traces = create_pitch()
    for pass_obj in player_passes:

        start_location = pass_obj["location"]
        end_location = pass_obj["pass"]["end_location"]


        # If 'recipient' key exists, consider pass complete
        if "recipient" in pass_obj["pass"]:
            arrow_color = "rgba(128, 128, 128, 1)"
        else:
            # draw red arrow for incomplete passes
            arrow_color = "rgba(255, 0, 0, 0.75)"

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
                x=[start_location[0], end_location[0]],
                y=[start_location[1], end_location[1]],
                mode="lines",
                line={"width":2, "color":arrow_color},
                hoverinfo="none"  # Disable hover for the lines
            )
        )
        # Create individual points for pass start and end with hover text:
        text_str = f"{player_name}<br><br>Play pattern: "
        f"{pass_obj['play_pattern']['name']}<br>Recipient: {recipient_name}<br>"
        f"Body Part: {body_part}<br>Outcome: {outcome_name}"

        traces.append(
            go.Scatter(
                x=[start_location[0], end_location[0]],
                y=[start_location[1], end_location[1]],
                mode="markers",
                marker={"size": 5, "color":"rgba(128, 128, 128, 0.0)"},
                text=[text_str, text_str],
                hovertemplate="%{text}<extra></extra>"
            )
        )
        # Add an arrow annotation for the pass:
        annotations.append(
            {
                "y":end_location[1],
                "x":end_location[0],
                "ay":start_location[1],
                "ax":start_location[0],
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
                "size": 24,  # adjust as needed
                "family": "Arial, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200,
        height=800,
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[0, 120]
        },
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "range": [0, 80]
        },
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        annotations=annotations
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

    annotations = []

    traces = create_pitch()
    for shot_obj in player_shots:

        start_location = shot_obj["location"]
        end_location = shot_obj["shot"]["end_location"]


        # If outcome is Goal, set color to green
        if shot_obj["shot"]["outcome"]["name"] == "Goal":
            marker_color = "rgba(0, 255, 0, 0.75)"
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

        # Draw the shaft of the arrow as a line without hover text:
        traces.append(
            go.Scatter(
                x=[start_location[0]],
                y=[start_location[1]],
                mode="markers",
                line={
                    "width":4,
                    "color":marker_color
                },
                hoverinfo="none"  # Disable hover for the lines
            )
        )
        # Create individual points for pass start and end with hover text:
        text_str = f"{player_name} (xG: {statsbomb_xg:.2f})<br><br>Play pattern: "
        f"{shot_obj['play_pattern']['name']}<br>Recipient: {type_name}<br>Body Part: "
        f"{body_part}<br>Outcome: {outcome_name}<br>Technique: {technique_name}"

        traces.append(
            go.Scatter(
                x=[start_location[0]],
                y=[start_location[1]],
                mode="markers",
                marker={"size":1, "color": "rgba(128, 128, 128, 0.0)"},
                text=[text_str, text_str],
                hovertemplate="%{text}<extra></extra>"
            )
        )
        # Add an arrow annotation for the pass:
        annotations.append({
                "y":end_location[1],
                "x":end_location[0],
                "ay":start_location[1],
                "ax":start_location[0],
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
                "size": 24,  # adjust as needed
                "family": "Arial, bold"
            },
            "xanchor": "center",
            "yanchor": "top"
        },
        showlegend=False,
        autosize=False,
        width=1200,
        height=800,
        xaxis={
            "showgrid":False,
            "zeroline":False,
            "showticklabels":False,
            "range":[0, 120]
        },
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "range":[0, 80]
        },
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
        annotations=annotations  # Include the annotations here
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
            fillcolor="rgba(255, 0, 0, 0.75)",
            line={"color":"rgba(255, 0, 0, 0.75)"}
        ),
        # go.Scatterpolar(
        #     r=list(opp_event_count.values()),
        #     theta=list(opp_event_count.keys()),
        #     fill='toself',
        #     name='Opponent Events',
        #     fillcolor='rgba(128, 128, 128, 0.75)',
        #     line=dict(color='rgba(128, 128, 128, 0.75)')
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
                    "color":"rgba(128, 128, 128, 1)"
                }
            }
       },
        plot_bgcolor="rgba(20, 20, 20, 0.9)",
        paper_bgcolor="rgba(20, 20, 20, 0.9)",
    )

    return {"data": data, "layout": layout}

# @app.callback(
#     Output('player-id-output', 'children'),
#     [Input('player-dropdown', 'value')]
# )
# def update_player_id(selected_player_id):
#     return f'Player ID: {selected_player_id}'


app.layout = html.Div(children=[
    html.Div(className="header-section", children=[
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
    html.Div(className="pitch-graphs-section", children=[

        html.Div(className="pass-network-section", children=[
            dcc.Graph(
                id="pass-network-graph",
                figure={
                    "data": [],
                    "layout": default_layout
                },
                config={"displayModeBar": False}
            ),
        ]),
    ]),
        html.Div(className="player-passes-section", children=[
        dcc.Graph(
            id="player-passes-graph",
            figure={
                "data": [],
                "layout": default_layout
            },
            config={"displayModeBar": False}
        ),
    ]),
    html.Div(className="shots-section", children=[
        dcc.Graph(
            id="shots-graph",
            figure={
                "data": [],
                "layout": default_layout
            },
            config={"displayModeBar": False}
        ),
    ]),
    html.Div(className="radar-section", children=[
        dcc.Graph(
            id="radar-chart",
            figure={
                "data": [],
                "layout": default_layout
            },
            config={"displayModeBar": False}
        ),
    ]),
    # html.Div([
    #     html.H1('Multi-page app with Dash Pages'),
    #     html.Div([
    #         html.Div(
    #             dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"])
    #         ) for page in dash.page_registry.values()
    #     ]),
    #     dash.page_container
    # ])


], style={"backgroundColor": "rgba(20, 20, 20, 0.9)"})




if __name__ == "__main__":
    app.run_server(debug=True)
