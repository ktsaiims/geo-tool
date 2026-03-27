from pathlib import Path


root_dir = Path.cwd()

PATHS = {
    'root': root_dir,
    'data': root_dir / 'geo_tool_data',
    'logs': root_dir / 'geo_tool_logs',
    'secrets': root_dir / 'geo_tool_secrets'
}
