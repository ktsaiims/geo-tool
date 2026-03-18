import os
from datetime import datetime

os.environ['TIMESTAMP'] = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
os.environ['LOG_LEVEL'] = 'DEBUG'
