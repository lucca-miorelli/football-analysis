import pandas as pd
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from mplsoccer import Pitch, FontManager

from football_analysis.config.constant import (
    FORMATION_DICT,
    MIN_TRANSPARENCY,
    MAX_LINE_WIDTH,
    MAX_MARKER_SIZE
)

class PassAnalysis:
    def __init__(self, events_file_name=None, team_id=None):
        self.file_path = os.path.join('data', events_file_name)
        self.team_id = team_id
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)

    def get_team_passes(self):
        match_passes = [x for x in self.data if x['type']['id'] == 30]
        self.team_passes = [x for x in match_passes if x['team']['id'] == self.team_id]
        print(self.team_passes[10])

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
                "possession_team_id": [i["possession_team"]["id"] for i in self.team_passes],
                "possession_team_name": [i["possession_team"]["name"] for i in self.team_passes],
                "play_pattern_id": [i["play_pattern"]["id"] for i in self.team_passes],
                "play_pattern_name": [i["play_pattern"]["name"] for i in self.team_passes],
                "team_id": [i["team"]["id"] for i in self.team_passes],
                "team_name": [i["team"]["name"] for i in self.team_passes],
                "player_id": [i["player"]["id"] for i in self.team_passes],
                "player_name": [i["player"]["name"] for i in self.team_passes],
                "position_id": [i["position"]["id"] for i in self.team_passes],
                "position_name": [i["position"]["name"] for i in self.team_passes],
                "location_x": [i["location"][0] for i in self.team_passes],
                "location_y": [i["location"][1] for i in self.team_passes],
                "duration": [i["duration"] for i in self.team_passes],
                "pass_recipient_id": [i["pass"].get("recipient", {}).get("id", None) for i in self.team_passes],
                "pass_recipient_name": [i["pass"].get("recipient", {}).get("name", None) for i in self.team_passes],
                "pass_length": [i["pass"]["length"] for i in self.team_passes],
                "pass_angle": [i["pass"]["angle"] for i in self.team_passes],
                "pass_height_id": [i["pass"]["height"]["id"] for i in self.team_passes],
                "pass_height_name": [i["pass"]["height"]["name"] for i in self.team_passes],
                "pass_end_location_x": [i["pass"]["end_location"][0] for i in self.team_passes],
                "pass_end_location_y": [i["pass"]["end_location"][1] for i in self.team_passes], 
                "pass_outcome_id": [i["pass"].get("outcome", {}).get("id", None) for i in self.team_passes],
                "pass_outcome_name": [i["pass"].get("outcome", {}).get("name", None) for i in self.team_passes],
            }
        )
        print(self.team_passes_df.head())
        # Print unique team names
        print(self.team_passes_df['team_name'].unique())

    
    def get_players_df(self):
        players = []

        # iterate over the events data (replace events_data with your actual data variable)
        for event in self.team_passes:
            if 'tactics' in event:
                team_id = event['team']['id']
                team_name = event['team']['name']
                formation = event['tactics']['formation']
                
                # iterate over the lineup
                for player in event['tactics']['lineup']:
                    player_id = player['player']['id']
                    player_name = player['player']['name']
                    position_id = player['position']['id']
                    position_name = player['position']['name']
                    jersey_number = player['jersey_number']
                    
                    # append player data to the list
                    players.append([player_id, player_name, position_id, position_name, jersey_number, team_id, team_name, formation])

        # create dataframe
        self.players_df = pd.DataFrame(players, columns=['player_id', 'player_name', 'position_id', 'position_name', 'jersey_number', 'team_id', 'team_name', 'formation'])

        formation_dict = {1: 'GK', 2: 'RB', 3: 'RCB', 4: 'CB', 5: 'LCB', 6: 'LB', 7: 'RWB',
                  8: 'LWB', 9: 'RDM', 10: 'CDM', 11: 'LDM', 12: 'RM', 13: 'RCM',
                  14: 'CM', 15: 'LCM', 16: 'LM', 17: 'RW', 18: 'RAM', 19: 'CAM',
                  20: 'LAM', 21: 'LW', 22: 'RCF', 23: 'ST', 24: 'LCF', 25: 'SS'}

        self.players_df['position_abbreviation'] = self.players_df.position_id.map(formation_dict)

        print(self.players_df.head())
    
    def get_passers_avg_location(self):
        passers_avg_location = self.team_passes_df.groupby(['player_id']).agg(
            {
                'location_x': 'mean',
                'location_y': 'mean',
                'id': 'count'
            }
        ).reset_index().rename(columns={'location_x': 'x', 'location_y': 'y', 'id': 'passes_given'})

        recipients_count = self.team_passes_df.groupby(['pass_recipient_id']).agg(
            {
                'id': 'count'
            }
        ).reset_index().rename(columns={'id': 'passes_received'})

        # merge the two dataframes
        passers_avg_location = passers_avg_location.merge(recipients_count, left_on='player_id', right_on='pass_recipient_id', how='left').drop(columns=['pass_recipient_id'])
        # Sum the passes given and received
        passers_avg_location['total_passes'] = passers_avg_location['passes_given'] + passers_avg_location['passes_received']
        # Force player_id to string
        passers_avg_location['player_id'] = passers_avg_location['player_id'].astype(str)

        self.passers_avg_location = passers_avg_location

        print(self.passers_avg_location.head())
    
    def get_passes_between_players(self):
        # create a temporary dataframe with sorted player_id and pass_recipient_id
        temp_df = self.team_passes_df[['player_id', 'pass_recipient_id']].apply(lambda x: sorted(x), axis=1, result_type='expand')

        # rename the columns
        temp_df.columns = ['player1', 'player2']

        # add the 'id' column from the original dataframe
        temp_df['id'] = self.team_passes_df['id']

        # now groupby 'player1' and 'player2' and count the number of 'id'
        passes_between = temp_df.groupby(['player1', 'player2']).agg(
            {
                'id': 'count'
            }
        ).reset_index()

        # rename the columns back to 'player_id' and 'pass_recipient_id'
        passes_between.rename(columns={'player1': 'player_id', 'player2': 'pass_recipient_id', 'id': 'pass_count'}, inplace=True)

        # Transform player_id and pass_rcipient_id back to string, without .0
        passes_between['player_id'] = passes_between['player_id'].astype(int).astype(str)
        passes_between['pass_recipient_id'] = passes_between['pass_recipient_id'].astype(int).astype(str)

        self.passes_between = passes_between

        print(self.passes_between.head())
    
    def enrich_passes_between_players(self):
        self.passes_between = (
            self.passes_between
                .merge(self.passers_avg_location[["player_id", "x", "y"]], left_on='player_id', right_on='player_id', how='left')
                .merge(self.passers_avg_location[["player_id", "x", "y"]].rename(columns={"x":"x_end", "y":"y_end"}), left_on='pass_recipient_id', right_on='player_id', how='left')
                .drop(columns='player_id_y')
                .rename(columns={'player_id_x': 'player_id'})
        )

        print(self.passes_between.head())

    
    def plot_pass_network(self):
        color = np.array(to_rgba('white'))
        color = np.tile(color, (len(self.passes_between), 1))
        c_transparency = self.passes_between.pass_count / self.passes_between.pass_count.max()
        c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
        color[:, 3] = c_transparency

        TEAM = 'Bayer Leverkusen'
        OPPONENT = 'RB Leipzig'
        FORMATION = '343'
        self.passes_between['width'] = (self.passes_between.pass_count / self.passes_between.pass_count.max() *
                                MAX_LINE_WIDTH)
        self.passers_avg_location['marker_size'] = (self.passers_avg_location['total_passes']
                                                / self.passers_avg_location['total_passes'].max() * MAX_MARKER_SIZE)

        pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor("#22312b")
    

        fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0,
                            # Turn off the endnote/title axis. I usually do this after
                            # I am happy with the chart layout and text placement
                            axis=False,
                            title_space=0, grid_height=0.82, endnote_height=0.05)
        fig.set_facecolor("#22312b")
        pass_lines = pitch.lines(self.passes_between.x, self.passes_between.y,
                                self.passes_between.x_end, self.passes_between.y_end, lw=self.passes_between.width,
                                color=color, zorder=1, ax=axs['pitch'])
        pass_nodes = pitch.scatter(self.passers_avg_location.x, self.passers_avg_location.y,
                                s=self.passers_avg_location.marker_size,
                                color='#E32221', edgecolors='black', linewidth=1, alpha=1, ax=axs['pitch'])
        for index, row in self.passers_avg_location.iterrows():
            pitch.annotate(row.name, xy=(row.x, row.y), c='white', va='center',
                        ha='center', size=16, weight='bold', ax=axs['pitch'])

        # Load a custom font.
        URL = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf'
        robotto_regular = FontManager(URL)

        # endnote /title
        axs['endnote'].text(1, 0.5, '@your_twitter_handle', color='#c7d5cc',
                            va='center', ha='right', fontsize=15,
                            fontproperties=robotto_regular.prop)
        TITLE_TEXT = f'{TEAM}, {FORMATION} formation'
        axs['title'].text(0.5, 0.7, TITLE_TEXT, color='#c7d5cc',
                        va='center', ha='center', fontproperties=robotto_regular.prop, fontsize=30)
        axs['title'].text(0.5, 0.25, OPPONENT, color='#c7d5cc',
                        va='center', ha='center', fontproperties=robotto_regular.prop, fontsize=18)
        plt.show()

if __name__ == "__main__":
    pass_analysis = PassAnalysis(events_file_name='3895052.json', team_id=904)
    pass_analysis.get_team_passes()
    pass_analysis.get_pass_df()
    pass_analysis.get_players_df()
    pass_analysis.get_passers_avg_location()
    pass_analysis.get_passes_between_players()
    pass_analysis.enrich_passes_between_players()
    pass_analysis.plot_pass_network()