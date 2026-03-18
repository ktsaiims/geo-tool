from pathlib import Path


root_dir = Path(__file__).parent.parent

PATHS = {
    'root': root_dir,
    'data': root_dir / 'data',
    'logs': root_dir / 'logs'
}
