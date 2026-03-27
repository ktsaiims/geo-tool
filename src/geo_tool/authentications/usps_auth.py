import json
import logging
import time
from dotenv import load_dotenv, set_key
from geo_tool.classes.api.usps_client import UspsApiClient
from geo_tool.paths import PATHS
from os import getenv
from pathlib import Path


logger = logging.getLogger(__name__)

def save_access_token(token_data: str) -> Path:
    '''Save the USPS access token as a JSON file.

    Args:
        token_data: The access token string in JSON format

    Returns:
        Path: Access token path
    '''
    token_path = PATHS['secrets'] / 'usps_token.json'
    with token_path.open('w', encoding='utf-8') as f:
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
    env_path = PATHS['secrets'] / '.env'
    set_key(
        dotenv_path=env_path,
        key_to_set='USPS_ACCESS_TOKEN',
        value_to_set=access_token_str
    )
    logger.debug(f'Access token string written into: {env_path}')

    load_dotenv(dotenv_path=env_path, override=True) # reload .env variables
    logger.debug('Reloaded .env variables')

def is_token_valid() -> bool:
    '''Check if token exists or has expired.'''
    json_token = PATHS['secrets'] / 'usps_token.json'

    if not json_token.exists():
        logger.warning(f'Could not find token: {json_token}')
        return False

    with json_token.open('r') as f:
        token_data = json.load(f)

    expiration_time = token_data['issued_at'] + token_data['expires_in'] # milliseconds since Unix epoch
    current_time = time.time() * 1000 # current time in milliseconds

    if current_time < expiration_time:
        logger.info('Token is valid')
        return True
    else:
        logger.warning('Token expired')
        return False

def request_access_token(client_id: str, client_secret: str):
    '''Request an access token from USPS API and save it to .env file.

    Args:
        client_id: USPS client ID
        client_secret: USPS client secret
    '''
    usps_client = UspsApiClient(client_id=client_id, client_secret=client_secret)
    token_data = usps_client.get_access_token()
    access_token_path = save_access_token(token_data)
    write_access_token_to_env(access_token_path)
    getenv('USPS_ACCESS_TOKEN')

def validate_usps_authentication() -> str | None:
    '''Validation flow for USPS authentication.

    Returns:
        access_token: USPS access token string
    '''
    logger.debug('Validating USPS authentication...')

    access_token = getenv('USPS_ACCESS_TOKEN')
    client_id = getenv('USPS_CLIENT_ID')
    client_secret = getenv('USPS_CLIENT_SECRET')

    # Check if token exists or if it's expired
    if not access_token or not is_token_valid():
        logger.warning('Invalid USPS access token')

        if not client_id or not client_secret:
            err_msg = 'Cannot retrieve an USPS access token - USPS client ID and/or client secret is missing from .env file'
            logger.error(err_msg)
            raise EnvironmentError(err_msg)

        request_access_token(client_id=client_id, client_secret=client_secret)

    logger.debug('USPS access token found')

    return access_token
