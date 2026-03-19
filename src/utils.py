import logging
import sys
from configs import LOG_LEVEL, TIMESTAMP
from pathlib import Path
from src.paths import PATHS


logger = logging.getLogger(__name__)

def setup(paths: dict):
    '''Set up directories and logging

    Args:
        paths (dict): Directory paths
    '''
    # Ensure directory paths exist
    for path in paths.values():
        Path(path).mkdir(parents=True, exist_ok=True)

    # Set up logging
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

    logger.info('Setup complete')
