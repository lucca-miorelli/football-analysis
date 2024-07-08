import json
import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from mplsoccer import FontManager, Pitch

from football_analysis.config.constant import (
    MAX_LINE_WIDTH,
    MAX_MARKER_SIZE,
    MIN_TRANSPARENCY,
)


class PassAnalysis:
    def __init__(self, game_id=None, team_id=None, starting_players_only: bool = True):
        self.file_path = os.path.join("data", "events", game_id + ".json")
        self.team_id = team_id
        with open(self.file_path) as f:
            self.data = json.load(f)
        self.players_to_plot = [
            str(player["player"]["id"])
            for x in self.data[:2]
            if "tactics" in x
            and "lineup" in x["tactics"]  # Only Starting XI
            and x["team"]["id"] == team_id
            for player in x["tactics"]["lineup"]
        ]
        if not starting_players_only:
            replacements = [
                str(x["substitution"]["replacement"]["id"])
                for x in self.data
                if x["type"]["id"] == 19
            ]
            self.players_to_plot = self.players_to_plot + replacements
        # #print(self.players_to_plot)
        self.team_name = [
            x["team"]["name"] for x in self.data[:2] if x["team"]["id"] == team_id
        ][0]
        self.team_formation = [
            str(x["tactics"]["formation"])
            for x in self.data[:2]
            if x["team"]["id"] == team_id
        ][0]
        self.opp_team_name = [
            x["team"]["name"] for x in self.data[:2] if x["team"]["id"] != team_id
        ][0]
        self.get_team_passes()
        self.get_pass_df()
        self.get_players_df()
        self.get_passers_avg_location()
        self.get_passes_between_players()
        self.enrich_passes_between_players()

    def get_player_passes(self, player_id):
        player_passes = [x for x in self.team_passes if x["player"]["id"] == player_id]
        return player_passes

    def get_team_passes(self):
        match_passes = [x for x in self.data if x["type"]["id"] == 30]
        self.team_passes = [x for x in match_passes if x["team"]["id"] == self.team_id]
        # print(self.team_passes[10])
        # print(len(self.team_passes))

    def get_pass_df(self):
        self.team_passes_df = pd.DataFrame(
            {
                "id": [i["id"] for i in self.team_passes],
                "index": [i["index"] for i in self.team_passes],
                "period": [i["period"] for i in self.team_passes],
                "timestamp": [i["timestamp"] for i in self.team_passes],
                "minute": [i["minute"] for i in self.team_passes],
                "second": [i["second"] for i in self.team_passes],
                "type_name": [i["type"]["name"] for i in self.team_passes],
                "type_id": [i["type"]["id"] for i in self.team_passes],
                "possession": [i["possession"] for i in self.team_passes],
                "possession_team_id": [
                    i["possession_team"]["id"] for i in self.team_passes
                ],
                "possession_team_name": [
                    i["possession_team"]["name"] for i in self.team_passes
                ],
                "play_pattern_id": [i["play_pattern"]["id"] for i in self.team_passes],
                "play_pattern_name": [
                    i["play_pattern"]["name"] for i in self.team_passes
                ],
                "team_id": [i["team"]["id"] for i in self.team_passes],
                "team_name": [i["team"]["name"] for i in self.team_passes],
                "player_id": [i["player"]["id"] for i in self.team_passes],
                "player_name": [i["player"]["name"] for i in self.team_passes],
                "position_id": [i["position"]["id"] for i in self.team_passes],
                "position_name": [i["position"]["name"] for i in self.team_passes],
                "location_x": [i["location"][0] for i in self.team_passes],
                "location_y": [i["location"][1] for i in self.team_passes],
                "duration": [i["duration"] for i in self.team_passes],
                "pass_recipient_id": [
                    i["pass"].get("recipient", {}).get("id", None)
                    for i in self.team_passes
                ],
                "pass_recipient_name": [
                    i["pass"].get("recipient", {}).get("name", None)
                    for i in self.team_passes
                ],
                "pass_length": [i["pass"]["length"] for i in self.team_passes],
                "pass_angle": [i["pass"]["angle"] for i in self.team_passes],
                "pass_height_id": [i["pass"]["height"]["id"] for i in self.team_passes],
                "pass_height_name": [
                    i["pass"]["height"]["name"] for i in self.team_passes
                ],
                "pass_end_location_x": [
                    i["pass"]["end_location"][0] for i in self.team_passes
                ],
                "pass_end_location_y": [
                    i["pass"]["end_location"][1] for i in self.team_passes
                ],
                "pass_outcome_id": [
                    i["pass"].get("outcome", {}).get("id", None)
                    for i in self.team_passes
                ],
                "pass_outcome_name": [
                    i["pass"].get("outcome", {}).get("name", None)
                    for i in self.team_passes
                ],
            }
        )
        # print(self.team_passes_df.head())
        # #print unique team names
        # print(self.team_passes_df['team_name'].unique())

    def get_players_df(self):
        players = []

        # iterate over the events data (replace events_data with your actual data variable)
        for event in self.data[:2]:
            if "tactics" in event:
                team_id = event["team"]["id"]
                team_name = event["team"]["name"]
                formation = event["tactics"]["formation"]

                # iterate over the lineup
                for player in event["tactics"]["lineup"]:
                    player_id = player["player"]["id"]
                    player_name = player["player"]["name"]
                    position_id = player["position"]["id"]
                    position_name = player["position"]["name"]
                    jersey_number = player["jersey_number"]

                    # append player data to the list
                    players.append(
                        [
                            player_id,
                            player_name,
                            position_id,
                            position_name,
                            jersey_number,
                            team_id,
                            team_name,
                            formation,
                        ]
                    )

        # create dataframe
        self.players_df = pd.DataFrame(
            players,
            columns=[
                "player_id",
                "player_name",
                "position_id",
                "position_name",
                "jersey_number",
                "team_id",
                "team_name",
                "formation",
            ],
        )

        formation_dict = {
            1: "GK",
            2: "RB",
            3: "RCB",
            4: "CB",
            5: "LCB",
            6: "LB",
            7: "RWB",
            8: "LWB",
            9: "RDM",
            10: "CDM",
            11: "LDM",
            12: "RM",
            13: "RCM",
            14: "CM",
            15: "LCM",
            16: "LM",
            17: "RW",
            18: "RAM",
            19: "CAM",
            20: "LAM",
            21: "LW",
            22: "RCF",
            23: "ST",
            24: "LCF",
            25: "SS",
        }

        self.players_df["position_abbreviation"] = self.players_df.position_id.map(
            formation_dict
        )
        self.players_df["player_id"] = self.players_df["player_id"].astype(str)

        # print(self.players_df.head())

    def get_passers_avg_location(self):
        passers_avg_location = (
            self.team_passes_df.groupby(["player_id"])
            .agg({"location_x": "mean", "location_y": "mean", "id": "count"})
            .reset_index()
            .rename(
                columns={"location_x": "x", "location_y": "y", "id": "passes_given"}
            )
        )

        recipients_count = (
            self.team_passes_df.groupby(["pass_recipient_id"])
            .agg({"id": "count"})
            .reset_index()
            .rename(columns={"id": "passes_received"})
        )

        # merge the two dataframes
        passers_avg_location = passers_avg_location.merge(
            recipients_count,
            left_on="player_id",
            right_on="pass_recipient_id",
            how="left",
        ).drop(columns=["pass_recipient_id"])
        # Sum the passes given and received
        passers_avg_location["total_passes"] = (
            passers_avg_location["passes_given"]
            + passers_avg_location["passes_received"]
        )
        # Force player_id to string
        passers_avg_location["player_id"] = passers_avg_location["player_id"].astype(
            str
        )

        self.passers_avg_location = passers_avg_location

        # print(self.passers_avg_location.head())

    def get_passes_between_players(self):
        # create a temporary dataframe with sorted player_id and pass_recipient_id
        temp_df = self.team_passes_df[["player_id", "pass_recipient_id"]].apply(
            lambda x: sorted(x), axis=1, result_type="expand"
        )

        # rename the columns
        temp_df.columns = ["player1", "player2"]

        # add the 'id' column from the original dataframe
        temp_df["id"] = self.team_passes_df["id"]

        # now groupby 'player1' and 'player2' and count the number of 'id'
        passes_between = (
            temp_df.groupby(["player1", "player2"]).agg({"id": "count"}).reset_index()
        )

        # rename the columns back to 'player_id' and 'pass_recipient_id'
        passes_between.rename(
            columns={
                "player1": "player_id",
                "player2": "pass_recipient_id",
                "id": "pass_count",
            },
            inplace=True,
        )

        # Transform player_id and pass_rcipient_id back to string, without .0
        passes_between["player_id"] = (
            passes_between["player_id"].astype(int).astype(str)
        )
        passes_between["pass_recipient_id"] = (
            passes_between["pass_recipient_id"].astype(int).astype(str)
        )

        self.passes_between = passes_between

        # print(self.passes_between.head())

    def enrich_passes_between_players(self):
        self.passes_between = (
            self.passes_between.merge(
                self.passers_avg_location[["player_id", "x", "y"]],
                left_on="player_id",
                right_on="player_id",
                how="left",
            )
            .merge(
                self.passers_avg_location[["player_id", "x", "y"]].rename(
                    columns={"x": "x_end", "y": "y_end"}
                ),
                left_on="pass_recipient_id",
                right_on="player_id",
                how="left",
            )
            .drop(columns="player_id_y")
            .rename(columns={"player_id_x": "player_id"})
        )

        # print(self.passes_between.head())

    def plot_pass_network(self):
        # Define the minimum and maximum font size for the jersey number annotations
        MIN_FONT_SIZE = 10
        MAX_FONT_SIZE = 20

        self.passes_between["width"] = (
            self.passes_between.pass_count
            / self.passes_between.pass_count.max()
            * MAX_LINE_WIDTH
        )
        self.passers_avg_location["marker_size"] = (
            self.passers_avg_location["total_passes"]
            / self.passers_avg_location["total_passes"].max()
            * MAX_MARKER_SIZE
        )
        # Normalize marker_size to get values between 0 and 1
        self.passers_avg_location["normalized_marker_size"] = (
            self.passers_avg_location["marker_size"]
            / self.passers_avg_location["marker_size"].max()
        )

        # Scale normalized_marker_size to get font sizes between MIN_FONT_SIZE and MAX_FONT_SIZE
        self.passers_avg_location["font_size"] = (
            MIN_FONT_SIZE
            + self.passers_avg_location["normalized_marker_size"]
            * (MAX_FONT_SIZE - MIN_FONT_SIZE)
        )
        pitch = Pitch(
            pitch_type="statsbomb", pitch_color="#22312b", line_color="#c7d5cc"
        )
        fig, ax = pitch.draw(
            figsize=(16, 11), constrained_layout=True, tight_layout=False
        )
        fig.set_facecolor("#22312b")

        fig, axs = pitch.grid(
            figheight=10,
            title_height=0.08,
            endnote_space=0,
            # Turn off the endnote/title axis. I usually do this after
            # I am happy with the chart layout and text placement
            axis=False,
            title_space=0,
            grid_height=0.82,
            endnote_height=0.05,
        )
        fig.set_facecolor("#22312b")

        # Filter only starting players
        temp_passes_between = self.passes_between.loc[
            (self.passes_between.player_id.isin(self.players_to_plot))
            & (self.passes_between.pass_recipient_id.isin(self.players_to_plot))
        ]
        temp_passers_avg_location = self.passers_avg_location.loc[
            self.passers_avg_location.player_id.isin(self.players_to_plot)
        ]
        # print(type(temp_passers_avg_location.player_id[0]))
        temp_passers_avg_location = temp_passers_avg_location.merge(
            self.players_df[
                [
                    "player_id",
                    "player_name",
                    "jersey_number",
                    "position_id",
                    "position_name",
                ]
            ],
            on="player_id",
            how="left",
        )
        # print(temp_passes_between.head())
        # print(temp_passers_avg_location.head())

        color = np.array(to_rgba("white"))
        color = np.tile(color, (len(temp_passes_between), 1))
        c_transparency = (
            temp_passes_between.pass_count / temp_passes_between.pass_count.max()
        )
        c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
        color[:, 3] = c_transparency

        # Pass lines
        pitch.lines(
            temp_passes_between.x,
            temp_passes_between.y,
            temp_passes_between.x_end,
            temp_passes_between.y_end,
            lw=temp_passes_between.width,
            color=color,
            zorder=1,
            ax=axs["pitch"],
        )
        # Passer nodes
        pitch.scatter(
            temp_passers_avg_location.x,
            temp_passers_avg_location.y,
            s=temp_passers_avg_location.marker_size,
            color="#E32221",
            edgecolors="black",
            linewidth=1,
            alpha=1,
            ax=axs["pitch"],
        )
        for index, row in temp_passers_avg_location.iterrows():
            # print(row.jersey_number, row.x, row.y)
            pitch.annotate(
                row.jersey_number,
                xy=(row.x, row.y),
                c="white",
                va="center",
                ha="center",
                size=row.font_size,
                weight="bold",
                ax=axs["pitch"],
            )

        # Load a custom font.
        URL = "https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf"
        robotto_regular = FontManager(URL)

        # endnote /title
        axs["endnote"].text(
            1,
            0.5,
            "Lucca Miorelli",
            color="#c7d5cc",
            va="center",
            ha="right",
            fontsize=15,
            fontproperties=robotto_regular.prop,
        )
        TITLE_TEXT = f"{self.team_name}, {self.team_formation} formation"
        axs["title"].text(
            0.5,
            0.7,
            TITLE_TEXT,
            color="#c7d5cc",
            va="center",
            ha="center",
            fontproperties=robotto_regular.prop,
            fontsize=30,
        )
        axs["title"].text(
            0.5,
            0.25,
            self.opp_team_name,
            color="#c7d5cc",
            va="center",
            ha="center",
            fontproperties=robotto_regular.prop,
            fontsize=18,
        )
        plt.show()

    def plotly_test_network(
        self,
        passes_between=None,
        passers_avg_location=None,
        players_to_plot=None,
        players_df=None,
    ):
        if passes_between is None:
            passes_between = self.passes_between
        if passers_avg_location is None:
            passers_avg_location = self.passers_avg_location
        if players_to_plot is None:
            players_to_plot = self.players_to_plot
        if players_df is None:
            players_df = self.players_df
        # Define the minimum and maximum font size for the jersey number annotations
        MIN_FONT_SIZE = 10
        MAX_FONT_SIZE = 20

        passes_between["width"] = (
            passes_between.pass_count / passes_between.pass_count.max() * MAX_LINE_WIDTH
        )
        passers_avg_location["marker_size"] = (
            passers_avg_location["total_passes"]
            / passers_avg_location["total_passes"].max()
            * MAX_MARKER_SIZE
        )
        # Normalize marker_size to get values between 0 and 1
        passers_avg_location["normalized_marker_size"] = (
            passers_avg_location["marker_size"]
            / passers_avg_location["marker_size"].max()
        )

        # Scale normalized_marker_size to get font sizes between MIN_FONT_SIZE and MAX_FONT_SIZE
        passers_avg_location["font_size"] = MIN_FONT_SIZE + passers_avg_location[
            "normalized_marker_size"
        ] * (MAX_FONT_SIZE - MIN_FONT_SIZE)

        # Filter only starting players
        temp_passes_between = passes_between.loc[
            (passes_between.player_id.isin(players_to_plot))
            & (passes_between.pass_recipient_id.isin(players_to_plot))
        ]
        temp_passers_avg_location = passers_avg_location.loc[
            passers_avg_location.player_id.isin(players_to_plot)
        ]
        # print(type(temp_passers_avg_location.player_id[0]))
        temp_passers_avg_location = temp_passers_avg_location.merge(
            players_df[
                [
                    "player_id",
                    "player_name",
                    "jersey_number",
                    "position_id",
                    "position_name",
                ]
            ],
            on="player_id",
            how="left",
        )
        # print(temp_passes_between.head())
        # print(temp_passers_avg_location.head())

        color = np.array(to_rgba("white"))
        color = np.tile(color, (len(temp_passes_between), 1))
        c_transparency = (
            temp_passes_between.pass_count / temp_passes_between.pass_count.max()
        )
        c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
        color[:, 3] = c_transparency

        return temp_passes_between, temp_passers_avg_location

    # if __name__ == "__main__":
    #     pass_analysis = PassAnalysis(
    #         game_id='3895194',
    #         team_id=904,
    #         starting_players_only=True
    #     )
    #     pass_analysis.plot_pass_network()


class ShotAnalysis:
    def __init__(self, game_id=None, team_id=None):
        self.file_path = os.path.join("data", "events", game_id + ".json")
        self.team_id = team_id
        with open(self.file_path) as f:
            self.data = json.load(f)
        self.team_name = [
            x["team"]["name"] for x in self.data[:2] if x["team"]["id"] == team_id
        ][0]
        self.opp_team_name = [
            x["team"]["name"] for x in self.data[:2] if x["team"]["id"] != team_id
        ][0]
        self.get_team_shots()
        # self.get_shots_df()
        # self.get_players_df()
        # self.get_shots_by_player()

    def get_team_shots(self):
        match_shots = [x for x in self.data if x["type"]["id"] == 16]
        self.team_shots = [x for x in match_shots if x["team"]["id"] == self.team_id]

    # def get_shots_df(self):
    #     self.team_shots_df = pd.DataFrame(
    #         {
    #             "id": [i["id"] for i in self.team_shots],
    #             "index": [i["index"] for i in self.team_shots],
    #             "period": [i["period"] for i in self.team_shots],
    #             "timestamp": [i["timestamp"] for i in self.team_shots],
    #             "minute": [i["minute"] for i in self.team_shots],
    #             "second": [i["second"] for i in self.team_shots],
    #             "type_name": [i["type"]["name"] for i in self.team_shots],
    #             "type_id": [i["type"]["id"] for i in self.team_shots],
    #             "possession": [i["possession"] for i in self.team_shots],
    #             "possession_team_id": [i["possession_team"]["id"] for i in self.team_shots],
    #             "possession_team_name": [i["possession_team"]["name"] for i in self.team_shots],
    #             "play_pattern_id": [i["play_pattern"]["id"] for i in self.team_shots],
    #             "play_pattern_name": [i["play_pattern"]["


class Event:
    def __init__(self, game_id: str, player_id: str | None = None):
        self.file_path = os.path.join("data", "events", game_id + ".json")
        with open(self.file_path) as f:
            self.data = json.load(f)
        self.player_id = player_id
        self.get_event_count()

    def get_event_count(self):
        team_events = [
            x
            for x in self.data
            if isinstance(x, dict)
            and x.get("possession_team", {}).get("id") == 904
            and x["type"]["name"]
            in [
                "Miscontrol",
                "Block",
                "Foul Committed",
                "Foul Won",
                "Interception",
                "Ball Recovery",
                "Shot",
                "Goal Keeper",
                "Duel",
                "Clearance",
                "Dribble",
                "Dispossessed",
                "Dribbled Past",
                # 'Injury Stoppage',
                # 'Shield',
                "Bad Behaviour",
                # '50/50'
            ]
        ]

        opponent_events = [
            x
            for x in self.data
            if isinstance(x, dict)
            # and x.get('possession_team', {}).get('id') != 904
            and x["type"]["name"]
            in [
                "Miscontrol",
                "Block",
                "Foul Committed",
                "Foul Won",
                "Interception",
                "Ball Recovery",
                "Shot",
                "Goal Keeper",
                "Duel",
                "Clearance",
                "Dribble",
                "Dispossessed",
                "Dribbled Past",
                # 'Injury Stoppage',
                # 'Shield',
                "Bad Behaviour",
                # '50/50'
            ]
        ]

        if self.player_id is not None:
            # Filter team_events by player_id
            team_events = [
                x
                for x in team_events
                if x.get("player", {}).get("id", None) == int(self.player_id)
            ]

            # Filter opponent_events by player_id (so it gets filtered out)
            opponent_events = [
                x
                for x in opponent_events
                if x.get("player", {}).get("id", None) == int(self.player_id)
            ]

        self.event_count = dict(Counter([x["type"]["name"] for x in team_events]))
        self.opp_event_count = dict(
            Counter([x["type"]["name"] for x in opponent_events])
        )

        # sort the dictionary alphabetically
        self.event_count = dict(sorted(self.event_count.items()))
        self.opp_event_count = dict(sorted(self.opp_event_count.items()))

    # def pass_events(self):
    #     team_events = [
    #         x
    #         for x in self.data
    #         if isinstance(x, dict)
    #         and x.get('possession_team', {}).get('id') == 904
    #         and x['type']['name'] == 'Pass'
    #     ]

    #     opponent_events = [
    #         x
    #         for x in self.data
    #         if isinstance(x, dict)
    #         # and x.get('possession_team', {}).get('id') != 904
    #         and x['type']['name'] == 'Pass'
    #     ]

    #     if self.player_id is not None:
    #         # Filter team_events by player_id
    #         team_events = [
    #             x
    #             for x in team_events
    #             if x.get('player', {}).get('id', None) == int(self.player_id)
    #         ]

    #         # Filter opponent_events by player_id (so it gets filtered out)
    #         opponent_events = [
    #             x
    #             for x in opponent_events
    #             if x.get('player', {}).get('id', None) == int(self.player_id)
    #         ]

    #     status_count = dict(
    #         Counter([
    #             x.get('outcome').get('name') if isinstance(x.get('outcome'), dict) else 'Complete' for x in team_events
    #         ])
    #     )

    #     self.pass_status_count = dict(sorted(status_count.items()))


class MatchInfo:
    def __init__(self, game_id: str | None = None):
        self.game_id = game_id
        if game_id is not None:
            data = pd.read_json(os.path.join("data", "matches", "9", "281.json"))
            self.data = data.loc[data.match_id == int(game_id)]
            self.get_match_info()

    def get_match_info(self):
        self.match_info = {
            "home_team": self.data.home_team.values[0],
            "away_team": self.data.away_team.values[0],
            "home_score": self.data.home_score.values[0],
            "away_score": self.data.away_score.values[0],
            "competition": self.data.competition.values[0],
            "season": self.data.season.values[0],
            "kick_off": self.data.kick_off.values[0],
            "metadata": self.data.metadata.values[0],
            "stadium": self.data.stadium.values[0],
            "referee": self.data.referee.values[0],
        }
        print(self.match_info)
        return self.match_info
