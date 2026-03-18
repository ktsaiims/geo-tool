import json
import logging
import requests
from dataclasses import dataclass
from pathlib import Path
from src.paths import PATHS


logger = logging.getLogger(__name__)

@dataclass
class UspsApiClient:
    '''Client for interacting with USPS API.

    Attributes:
        client_id (str): USPS-provided client ID
        client_secret (str): USPS-provided client secret
        access_token (str): Access token saved in .env
    '''
    client_id: str | None=None
    client_secret: str | None=None
    access_token: str | None=None

    BASE_URL = 'https://apis.usps.com'
    TOKEN_URL = f'{BASE_URL}/oauth2/v3'
    ADDRESSES_URL = f'{BASE_URL}/addresses/v3'

    def save_access_token(self, token_data: str) -> Path:
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

    def get_access_token(self) -> str:
        '''Retrieve an access token from the USPS API using client credentials.

        Returns:
            str: The access token string in JSON format
        '''
        parameters = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        logger.info('Requesting USPS access token...')

        try:
            response = requests.post(
                url=f'{self.TOKEN_URL}/token',
                data=parameters,
                headers=headers
            )
            response.raise_for_status()
            logger.info('Received access token')

            return response.json()

        except Exception as e:
            logger.error(e)
            raise

    def get_city_state(self, zipcode: str) -> object:
        if self.access_token is None:
            print('Missing access token')
            raise

        parameters = {'ZIPCode': zipcode}
        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.get(
            url=f'{self.ADDRESSES_URL}/city-state',
            params=parameters,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
