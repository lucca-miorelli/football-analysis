import json
import pandas
import os

def process_data(
    data_folder:str='data/events/',
    output_folder:str='data/processed/'
):
    """
    Process data from StatsBomb repository.
    
    Args:
    data_folder (str): Local folder to read data from
    output_folder (str): Local folder to save data
    
    Returns:
    None
    """
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of files in data folder
    files = os.listdir(data_folder)
    print(f"Processing {len(files)} event files")
    
    match_dfs = []
    for file in files[:]:
        # Read json file
        with open(f'{data_folder}{file}', 'r') as f:
            data = json.load(f)
        
        # Create dataframe
        df = pandas.DataFrame(data)
        df['match_id'] = file.replace('.json', '')
        
        # Save as csv file
        output_file = f'{output_folder}{file.replace(".json", ".csv")}'
        match_dfs.append(df)
        
    # Concatenate dataframes
    match_dfs = pandas.concat(match_dfs)

    # Save as parquet file
    output_file = f'{output_folder}all_matches_events.parquet'
    match_dfs.to_parquet(output_file, index=False)

    print(f"Saved {output_file}")

    return None

def process_data_360(
    data_folder:str='data/three-sixty/',
    output_folder:str='data/processed/'
):
    """
    Process three sixty data from StatsBomb repository.
    
    Args:
    data_folder (str): Local folder to read data from
    output_folder (str): Local folder to save data
    
    Returns:
    None
    """
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of files in data folder
    files = os.listdir(data_folder)
    print(f"Processing {len(files)} three-sixty files")
    
    match_dfs = []
    for file in files:
        # Read json file
        with open(f'{data_folder}{file}', 'r') as f:
            data = json.load(f)

        # Create dataframe
        df = pandas.DataFrame(data)
        df['match_id'] = file.replace('.json', '')

        match_dfs.append(df)
        
    # Concatenate dataframes
    match_dfs = pandas.concat(match_dfs)

    # Save as parquet file
    output_file = f'{output_folder}all_matches_360.parquet'
    match_dfs.to_parquet(output_file, index=False)

    print(f"Saved {output_file}")

    return None

def merge_data(
    output_folder:str='data/processed/'
):
    """
    Merge data from StatsBomb repository.
    
    Args:
    output_folder (str): Local folder to save data
    
    Returns:
    None
    """
    # Read data
    events = pandas.read_parquet(f'{output_folder}all_matches_events.parquet')
    events_360 = pandas.read_parquet(f'{output_folder}all_matches_360.parquet')

    print("Merge data...")
    
    # Merge data
    merged_data = events.merge(
        events_360,
        how='left',
        left_on=['match_id', 'id'],
        right_on=['match_id', 'event_uuid'],
        suffixes=('_events', '_360')
    )
    
    # Save as parquet file
    output_file = f'{output_folder}all_matches_merged.parquet'
    merged_data.to_parquet(output_file, index=False)

    print(f"Saved {output_file}")
    print(merged_data.head())
    print(merged_data.columns)
    
    return None



def main(
    output_folder:str='data/processed/'
):
    """
    Main function to process data from StatsBomb repository.
    
    Args:
    data_folder (str): Local folder to read data from
    output_folder (str): Local folder to save data
    
    Returns:
    None
    """
    process_data(
        data_folder='data/events/',
        output_folder=output_folder
    )
    process_data_360(
        data_folder='data/three-sixty/',
        output_folder=output_folder
    )
    merge_data(
        output_folder=output_folder
    )

    return None


if __name__ == '__main__':
    main()