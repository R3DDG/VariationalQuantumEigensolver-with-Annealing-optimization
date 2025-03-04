from rich.console import Console
from annealing_method_constants.file_paths import output_file_path

def console_and_print(console: Console, message):
    """
    Выводит результат выполнения программы в файл и консоль

    :param message: Сообщение для вывода
    """
    console.print(message)
    with open(output_file_path, "a", encoding="utf-8") as file:
        file.write(console.export_text() + "\n")
