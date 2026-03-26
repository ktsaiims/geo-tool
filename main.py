import argparse
import configs
import logging
from src.paths import PATHS
from src.utils import setup
from src.routes import get_city_state_from_zip, get_coordinates_from_address

setup(paths=PATHS)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Get city/state or coordinates from a zip code.')

    # Positional args
    parser.add_argument('zipcode', help='5-digit zip code')

    # Flag args
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--citystate', action='store_true', help='Flag to get city/state')
    group.add_argument('--coordinates', action='store_true', help='Flag to get coordinates')
    group.required = True

    args = parser.parse_args()
    zip_code = args.zipcode

    if args.citystate:
        logger.debug('Flag --citystate')
        result = get_city_state_from_zip(zip_code=zip_code)
        print(f'city: {result.city}, state: {result.state}')

    elif args.coordinates:
        logger.debug('Flag --coordinates')
        result = get_coordinates_from_address(address=zip_code)
        print(f'latitude: {result.latitude}, longitude: {result.longitude}')

    else:
        logger.error('Error: failed to run')
        print('Error: failed to run. Use --help for more info.')

if __name__ == "__main__":
    main()
