import logging
import sys
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from geo_tool.paths import PATHS


logger = logging.getLogger(__name__)

def setup(is_verbose: bool=False):
    '''Set up directories and logging

    Args:
        is_verbose: Flag to trigger logger's DEBUG mode
    '''
    TIMESTAMP = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    # Ensure directory paths exist
    for path in PATHS.values():
        Path(path).mkdir(parents=True, exist_ok=True)

    # Set up logging
    if is_verbose:
        LOG_LEVEL = 'DEBUG'
    else:
        LOG_LEVEL = 'INFO'

    log_path = PATHS['logs'] / f'{TIMESTAMP}.log'
    logger.debug(f'Log level set to: {LOG_LEVEL}')

    handlers: list[logging.Handler] = [logging.FileHandler(log_path)]
    if LOG_LEVEL == 'DEBUG':
        handlers.append(logging.StreamHandler(sys.stdout)) # print logs to stdout in DEBUG mode

    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

    # Load .env
    load_dotenv(dotenv_path=PATHS['secrets'] / '.env')

    logger.debug('Initialized paths, logging, and .env')
    logger.info('Setup complete')
