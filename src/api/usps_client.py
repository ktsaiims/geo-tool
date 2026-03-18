import logging
import requests
from dataclasses import dataclass


logger = logging.getLogger(__name__)

@dataclass
class CityStateResults:
    '''Class to store the results of calling the `/city-state` endpoint.

    Attributes:
        city (str): City name of the address
        state (str): 2-character state code of the address
        ZIPCode (str): 5-digit zip code of the address
    '''
    city: str
    state: str
    ZIPCode: str

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

        logger.debug('Requesting USPS access token...')

        try:
            response = requests.post(
                url=f'{self.TOKEN_URL}/token',
                data=parameters,
                headers=headers
            )
            response.raise_for_status()
            logger.info('Received USPS access token')

            return response.json()

        except Exception as e:
            logger.error(e)
            raise

    def get_city_state(self, zipcode: str) -> CityStateResults:
        '''Retrieve city and state information for a given zip code.

        Args:
            zipcode (str): The 5-digit ZIP code to look up

        Returns:
            CityStateResults: A dataclass containing the city, state, and zip code
        '''
        if self.access_token is None:
            logger.error('USPS access token string not found in .env file')
            raise

        parameters = {'ZIPCode': zipcode}
        headers = {'Authorization': f'Bearer {self.access_token}'}

        try:
            response = requests.get(
                url=f'{self.ADDRESSES_URL}/city-state',
                params=parameters,
                headers=headers
            )
            response.raise_for_status()
            logger.debug(f'Received city/state results for zip code: {zipcode}')

            response = response.json()
            city_state_data = CityStateResults(**response)

            return city_state_data

        except Exception as e:
            logger.error(e)
            raise
