import requests
import json
import pandas as pd

from football_analysis.config.constant import (
    BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24,
    DATA_REPOSITORY_URL
)



def main(
    game_ids:list=BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24,
    data_repository_url:str=DATA_REPOSITORY_URL,
    local_data_folder:str='data/events/'

):
    for game_id in game_ids:
        print(f"Downloading {game_id=}")
        resp = requests.get(data_repository_url.format(game_id))
        data = json.loads(resp.text)

        # Save as json file in data folder
        file_path = f'{local_data_folder}{game_id}.json'

        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        print(f"Saved {game_id=}")


if __name__ == "__main__":
    main(
        game_ids=BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24,
        data_repository_url=DATA_REPOSITORY_URL,
        local_data_folder='data/events/'
    )

