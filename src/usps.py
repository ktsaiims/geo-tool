import json
import logging
from dotenv import load_dotenv, set_key
from pathlib import Path
from src.paths import PATHS


logger = logging.getLogger(__name__)

def save_access_token(token_data: str) -> Path:
    '''Save the USPS access token as a JSON file into the local root directory.

    Args:
        token_data (str): The access token string in JSON format

    Returns:
        Path: Access token path
    '''
    token_path = PATHS['root'] / 'usps_token.json'
    with open(token_path, 'w') as f:
        json.dump(token_data, f, indent=2)
        logger.info(f'USPS access token saved at: {token_path}')

    return token_path

def write_access_token_to_env(token_path: Path):
    '''Write USPS access token string to .env file.

    Args:
        token_path (Path): Path to access token JSON file
    '''
    with open(token_path, 'r') as f:
        json_data = json.load(f)

    access_token_str = json_data['access_token'].strip('"') # remove surrounding double-quotes
    env_path = PATHS['root'] / '.env'
    set_key(
        dotenv_path=env_path,
        key_to_set='USPS_ACCESS_TOKEN',
        value_to_set=access_token_str
    )

    load_dotenv(override=True) # refresh env variables
    logger.info('USPS access token string saved to .env file')
