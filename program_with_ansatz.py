import sys
import io
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

from utils.console_and_print import console_and_print
from utils.initialize_environment import initialize_environment
from utils.read_hamiltonian_data import read_hamiltonian_data
from utils.print_hamiltonian import print_hamiltonian
from utils.print_pauli_table import print_pauli_table
from utils.print_composition_table import print_composition_table
from utils.calculate_temp_steps import calculate_temp_steps
from vqa_utils.pauli_compose import pauli_compose
from vqa_utils.generate_shifted_theta import generate_shifted_theta
from vqa_utils.simulated_annealing import simulated_annealing
from vqa_utils.calculate_ansatz import calculate_ansatz
from vqa_utils.compute_uhu import compute_uhu
from vqa_utils.calculate_expectation import calculate_expectation
from constants.file_paths import HAMILTONIAN_FILE_PATH

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

def get_pauli_operators_from_user(console):
    console.print(Rule(":wave: Ввод операторов Паули для построения анзцаца:wave:"))
    
    while True:
        try:
            num_operators = int(console.input("[bold blue]Введите количество параметров для построения анзцаца: [/]"))
            if num_operators < 1:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]Ошибка: введите положительное целое число![/]")

    pauli_operators = []
    
    for i in range(num_operators):
        console.print(f"\n[bold green]Оператор {i+1}[/]")
        
        while True:
            try:
                coeff = float(1.0)
                indices_input = console.input("[bold blue]Индексы Паули через пробел (0 0 2 1): [/]").strip()
                indices = list(map(int, indices_input.split()))
                if any(x < 0 or x > 3 for x in indices):
                    raise ValueError("Индексы должны быть 0, 1, 2 или 3")
                pauli_operators.append((coeff, indices))
                break
            except ValueError as e:
                console.print(f"[bold red]Ошибка ввода: {e}. Попробуйте снова.[/]")
                
    return pauli_operators

def print_pauli_table(console, pauli_operators):
    table = Table(title="[bold blue]Таблица операторов Паули, используемых для построения анзаца[/]", show_header=True, header_style="bold")
    table.add_column("№", style="dim", width=3)
    table.add_column("Коэффициент", justify="right")
    table.add_column("Индексы Паули", justify="center")
    for i, (coeff, indices) in enumerate(pauli_operators, start=1):
        table.add_row(str(i), f"{coeff:.2f}", " ".join(map(str, indices)))
    console.print(table)

def main() -> None:
    console = initialize_environment()
    console.print(Rule(":computer: Начало работы программы :computer:"))
    pauli_operators = get_pauli_operators_from_user(console)
    if len(pauli_operators) < 2:
        console.print(Panel("[bold red]Ошибка: требуется минимум 2 оператора Паули![/]"))
        return
    if not HAMILTONIAN_FILE_PATH.exists():
        msg = (f"Файл [bold red]{HAMILTONIAN_FILE_PATH}[/] не найден!\n"
            "Убедитесь, что рядом с EXE есть папка [bold blue]params[/] с файлом [bold blue]hamiltonian_operators.txt[/].")
        console.print(Panel(msg, border_style="red"))
        return

    try:
        console.print("[bold green]Чтение гамильтониана...[/]")
        hamiltonian_operators, _ = read_hamiltonian_data(HAMILTONIAN_FILE_PATH)
        console.print("\n[bold blue]Гамильтониан:[/]")
        print_hamiltonian(console, hamiltonian_operators)
        print_pauli_table(console, pauli_operators)
        print_composition_table(console, pauli_compose, [op for _, op in pauli_operators])
    except ValueError as e:
            print(f"Ошибка импорта файла с описанием гамильтониана.")

    SA_PARAMS = {"initial_temp": 50.0, "cooling_rate": 0.98, "min_temp": 1e-6, "num_iterations_per_temp": 38, "step_size": 0.05}

    thermalization_steps = int(SA_PARAMS["num_iterations_per_temp"] * 0.2)
    temp_steps = calculate_temp_steps(SA_PARAMS["initial_temp"], SA_PARAMS["cooling_rate"], SA_PARAMS["min_temp"])
    total_steps = temp_steps * (thermalization_steps + SA_PARAMS["num_iterations_per_temp"])

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(bar_width=None),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),) as progress:
        task = progress.add_task("[cyan]Отжиг...", total=total_steps)
        optimized_theta, best_energy = simulated_annealing(initial_theta=generate_shifted_theta(pauli_operators),
            pauli_operators=pauli_operators, hamiltonian_operators=hamiltonian_operators,
            progress=progress, task=task, **SA_PARAMS)

    ansatz_dict, ansatz_symbolic, ansatz_numeric = calculate_ansatz(optimized_theta, pauli_operators)
    uhu_dict = compute_uhu(ansatz_dict, hamiltonian_operators)
    console.print(Panel(ansatz_symbolic, title="[bold green]Символьное представление анзаца[/]", border_style="green"))
    console.print(Panel(ansatz_numeric, title="[bold purple]Численное представление анзаца[/]", border_style="purple"))
    console.print(Panel(f"{best_energy:.6f}", title="[bold green]Энергия (<0|U†HU|0> для состояния |0...0>)[/]", border_style="green"))

    console.print(Rule(":sparkles: Вычисления завершены :sparkles:"))
    console.print("Нажмите Enter для выхода...")
    input()

if __name__ == "__main__":
    main()