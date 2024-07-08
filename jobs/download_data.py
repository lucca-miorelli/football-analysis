import json

import requests

from football_analysis.config.constant import (
    BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24,
    DATA_REPOSITORY_URL,
)
from football_analysis.statsbomb.scrape import AWS


def download_events_data(
    game_ids: list, data_repository_url: str, local_data_folder: str = "data/events/"
):
    """
    Download events data from StatsBomb repository

    Args:
    game_ids (list): List of game ids
    data_repository_url (str): URL to download data from
    local_data_folder (str): Local folder to save data

    Returns:
    None
    """
    for game_id in game_ids:
        print(f"Downloading {game_id=}")
        gh_folder = "events"
        resp = requests.get(data_repository_url.format(gh_folder, game_id))
        data = json.loads(resp.text)

        # Save as json file in data folder
        file_path = f"{local_data_folder}{game_id}.json"

        # with open(file_path, 'w') as f:
        #     json.dump(data, f)

        print(f"Saved {game_id=}")

        # Save to aws/minio
        aws = AWS()
        aws.save_to_json(data, gh_folder, game_id)


def download_match_metadata(
    data_repository_url: str, file_path: str = "data/matches/9/281.json"
):
    """
    Download match metadata from StatsBomb repository.

    Args:
    data_repository_url (str): URL to download data from
    file_path (str): Local file path to save data

    Returns:
    None
    """
    ##  Downloading match metadata
    matches_metadata = requests.get(data_repository_url.format("matches/9", "281"))

    matches_metadata = json.loads(matches_metadata.text)

    # Save as json file in data folder
    # with open(file_path, 'w') as f:
    #     json.dump(matches_metadata, f)

    print(f"Saved {file_path}")

    # Save to aws/minio
    aws = AWS()
    aws.save_to_json(matches_metadata, "matches/9", "281")


def download_three_sixty_data(
    game_ids: list,
    data_repository_url: str,
    local_data_folder: str = "data/three-sixty/",
):
    """
    Download three sixty data from StatsBomb repository.

    Args:
    game_ids (list): List of game ids
    data_repository_url (str): URL to download data from
    local_data_folder (str): Local folder to save data

    Returns:
    None
    """
    for game_id in game_ids:
        response = requests.get(data_repository_url.format("three-sixty", game_id))
        data = json.loads(response.text)

        # Save as json file in data folder
        file_path = f"{local_data_folder}{game_id}.json"

        # with open(file_path, 'w') as f:
        #     json.dump(data, f)

        print(f"Saved {file_path}")

        # Save to aws/minio
        aws = AWS()
        aws.save_to_json(data, "three-sixty", game_id)


def main(
    game_ids: list,
    data_repository_url: str,
):
    """
    Main function to download data from StatsBomb repository.

    Args:
    game_ids (list): List of game ids
    data_repository_url (str): URL to download data from

    Returns:
    None
    """
    download_events_data(game_ids=game_ids, data_repository_url=data_repository_url)
    download_match_metadata(data_repository_url=data_repository_url)
    download_three_sixty_data(
        game_ids=game_ids, data_repository_url=data_repository_url
    )


if __name__ == "__main__":

    main(
        game_ids=BAYER_LEVERKUSEN_GAMES_BUNDESLIGA_23_24[:],
        data_repository_url=DATA_REPOSITORY_URL,
    )
