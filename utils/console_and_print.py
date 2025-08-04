from rich.console import Console
from typing import Any
from constants.file_paths import OUTPUT_FILE_PATH

def console_and_print(console: Console, message: Any) -> None:
    console.print(message)
    with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(console.export_text() + "\n")
