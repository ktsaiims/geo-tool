import logging
from nt import access
from os import getenv
from src.GeographyResult import GeographyResult
from src.api.google_client import GoogleApiClient
from src.api.usps_client import UspsApiClient
from src.usps_auth import validate_usps_authentication


logger = logging.getLogger(__name__)

def get_city_state_from_zip(zip_code: str) -> GeographyResult:
    '''Logic route to get city/state info from a zip code.

    Args:
        zip_code: 5 or 9-digit zip code to search

    Returns:
        GeographyResult: A dataclass containing the zip code, city, and state
    '''
    logger.debug(f'Getting city/state from zip code: {zip_code}...')

    validate_usps_authentication()
    access_token = getenv('USPS_ACCESS_TOKEN')

    usps_client = UspsApiClient(access_token=access_token)
    result = usps_client.get_city_state(zipcode=zip_code)

    return GeographyResult(
        zip_code=result.ZIPCode,
        city=result.city,
        state=result.state,
        latitude=None,
        longitude=None
    )
