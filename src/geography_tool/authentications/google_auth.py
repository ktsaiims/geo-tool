import logging
from os import getenv


logger = logging.getLogger(__name__)

def validate_google_authentication() -> str | None:
    '''Validation flow for USPS authentication.

    Returns:
        google_api_key: Google API key string
    '''
    logger.debug('Validating Google authentication...')

    google_api_key = getenv('GOOGLE_API_KEY')

    if not google_api_key:
        err_msg = 'Google API key is missing from .env file'
        logger.error(err_msg)
        raise EnvironmentError(err_msg)

    logger.debug('Google API key found')

    return google_api_key
