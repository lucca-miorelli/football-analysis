from football_analysis.config.constant import (
    FORMATION_DICT, MIN_TRANSPARENCY, MAX_LINE_WIDTH, MAX_MARKER_SIZE
)
from football_analysis.statsbomb.analysis import PassAnalysis



pass_analysis = PassAnalysis(events_file_name='3895052.json', team_id=904)
pass_analysis.get_team_passes()
pass_analysis.get_pass_df()
pass_analysis.get_players_df()
pass_analysis.get_passers_avg_location()
pass_analysis.get_passes_between_players()
pass_analysis.enrich_passes_between_players()
pass_analysis.plot_pass_network()