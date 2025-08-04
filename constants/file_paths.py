import sys
from pathlib import Path

def get_base_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.argv[0]).parent
    else:
        return Path(__file__).parent.parent

HAMILTONIAN_FILE_PATH: Path = get_base_path() / "params" / "hamiltonian_operators.txt"
OUTPUT_FILE_PATH: Path = get_base_path() / "output.log"
