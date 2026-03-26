import json
import logging
from src.classes.api.usps_client import UspsApiClient
from dotenv import load_dotenv, set_key
from os import getenv
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

def validate_usps_authentication() -> str | None:
    '''Validation flow for USPS authentication.

    Returns:
        access_token: USPS access token string
    '''
    logger.debug('Validating USPS authentication...')

    access_token = getenv('USPS_ACCESS_TOKEN')
    client_id = getenv('USPS_CLIENT_ID')
    client_secret = getenv('USPS_CLIENT_SECRET')

    if not access_token:
        logger.warning('Missing USPS access token')

        if not client_id or not client_secret:
            logger.error('Cannot retrieve an USPS access token - USPS client ID and/or client secret is missing from .env file')
            raise

        usps_client = UspsApiClient(client_id=client_id, client_secret=client_secret)
        token_data = usps_client.get_access_token()
        access_token_path = save_access_token(token_data)
        write_access_token_to_env(access_token_path)
        access_token = getenv('USPS_ACCESS_TOKEN')

    logger.debug('USPS access token found')

    return access_token
