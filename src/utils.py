import logging
import os
import sys
from pathlib import Path
from src.paths import PATHS


logger = logging.getLogger(__name__)

def setup(paths: dict):
    '''Set up directories and logging

    Args:
        paths (dict): Directory paths
    '''
    logger.info('Setting up...')

    # Ensure directory paths exist
    for path in paths.values():
        Path(path).mkdir(parents=True, exist_ok=True)

    # Set up logging
    log_level = os.environ.get('LOG_LEVEL')
    log_path = PATHS['logs'] / f'{os.environ.get('TIMESTAMP')}.log'

    logger.debug(f'Log level set to: {log_level}')

    handlers = [logging.FileHandler(log_path)]
    if log_level == 'DEBUG':
        handlers.append(logging.StreamHandler(sys.stdout)) # print logs to stdout in DEBUG mode

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

    logger.info('Setup complete')
