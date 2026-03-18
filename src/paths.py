from pathlib import Paths


root_dir = Paths(__file__).parent.parent

PATHS = {
    'data': root_dir / 'data',
    'logs': root_dir / 'logs'
}
