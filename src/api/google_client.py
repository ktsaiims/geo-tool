import logging
import requests
from dataclasses import dataclass


logger = logging.getLogger(__name__)

@dataclass
class GeocodeResponse:
    '''A single geocoding result from Google Maps API.

    Attributes:
        address_components: List of address component dictionaries with long_name, short_name, and types.
        formatted_address: Human-readable formatted address string.
        location: Dictionary containing 'lat' and 'lng' coordinates.
        location_type: Accuracy level of the location (e.g., 'ROOFTOP', 'APPROXIMATE').
    '''
    address_components: list[dict]
    formatted_address: str
    location: dict
    location_type: str

@dataclass
class GeocodeResult:
    '''Class to store Google Maps geocoding API call.

    Attributes:
        results: List of GeocodeResponse objects containing geocoding results
        status: API response status (e.g., 'OK', 'ZERO_RESULTS', 'INVALID_REQUEST')
    '''
    results: list[GeocodeResponse]
    status: str

@dataclass
class GoogleApiClient:
    '''Client for interacting with Google Maps Geocoding API.

    Attributes:
        api_key: Google Maps API key for authentication
    '''
    api_key: str | None=None

    BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    def geocode_from_address(self, address: str, region: str='us') -> GeocodeResult:
        if self.api_key is None:
            logger.error('Google API key not found in .env file')
            raise

        parameters = {
            'key': self.api_key,
            'address': address,
            'region': region
        }

        try:
            response = requests.get(
                url=self.BASE_URL,
                params=parameters
            )
            response.raise_for_status()
            logger.debug(f'Received geocode results for address: {address}')

            response = response.json()

            results = []
            for r in response['results']:
                result = GeocodeResponse(
                    address_components=r['address_components'],
                    formatted_address=r['formatted_address'],
                    location=r['geometry']['location'],
                    location_type=r['geometry']['location_type'],
                )
                results.append(result)

            return GeocodeResult(results=results, status=response['status'])

        except Exception as e:
            logger.error(e)
            raise
