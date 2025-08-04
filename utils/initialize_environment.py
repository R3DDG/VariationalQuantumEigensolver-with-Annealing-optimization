from rich.console import Console
from constants.file_paths import OUTPUT_FILE_PATH

def initialize_environment() -> Console:
    if OUTPUT_FILE_PATH.exists():
        OUTPUT_FILE_PATH.unlink()
        
    return Console(force_terminal=True, color_system="truecolor", record=True)
