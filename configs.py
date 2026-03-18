from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

TIMESTAMP = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
LOG_LEVEL = 'DEBUG'
