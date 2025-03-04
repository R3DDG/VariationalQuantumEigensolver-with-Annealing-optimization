from rich.console import Console

# Путь к файлу для вывода результата
outputFilePath = "output.log"

def console_and_print(console: Console, message) -> None: 
    """
    Выводит результат выполнения программы в файл и консоль

    :param message: Сообщение для вывода
    """
    console.print(message)
    with open(outputFilePath, "a", encoding = "utf-8") as file:
        file.write(console.export_text() + "\n")