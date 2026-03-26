import logging
from src.classes.GeographyResult import GeographyResult
from src.classes.api.google_client import GoogleApiClient
from src.classes.api.usps_client import UspsApiClient
from src.google_auth import validate_google_authentication
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

    access_token = validate_usps_authentication()

    usps_client = UspsApiClient(access_token=access_token)
    result = usps_client.get_city_state(zipcode=zip_code)

    return GeographyResult(
        zip_code=result.ZIPCode,
        city=result.city,
        state=result.state
    )

def get_coordinates_from_address(address: str, country: str='us') -> GeographyResult:
    '''Logic route to get coordinates from a zip code.

    Args:
        address: Full address, zip code, or Google Plus Code
        country: ccTLD ("top-level domain") 2-character value

    Returns:
        GeographyResult: A dataclass containing the zip code, latitude, and longitude
    '''
    logger.debug(f'Getting coordinates from zip code: {address}...')

    api_key = validate_google_authentication()

    google_client = GoogleApiClient(api_key=api_key)
    result = google_client.geocode_from_address(address=address, region=country)
    geocode_response = result.results[0] # use first item in the list of GeocodeResponse

    latitude = geocode_response.location['lat']
    longitude = geocode_response.location['lng']

    return GeographyResult(
        zip_code=address,
        latitude=latitude,
        longitude=longitude
    )
