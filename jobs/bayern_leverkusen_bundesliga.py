from football_analysis.config.constant import (
    FORMATION_DICT, MIN_TRANSPARENCY, MAX_LINE_WIDTH, MAX_MARKER_SIZE
)
from football_analysis.statsbomb.analysis import PassAnalysis


pass_analysis_3895060 = PassAnalysis(
    game_id='3895302',
    team_id=904,
)
pass_analysis_3895060.plot_pass_network()

