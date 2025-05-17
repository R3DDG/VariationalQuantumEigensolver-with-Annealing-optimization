import sys
import io
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel

# Импорт самописных функций
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

# Импорт констант
from constants.file_paths import HAMILTONIAN_FILE_PATH

# Установка кодировки для корректного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def main():
    """Основная логика программы."""
    console = initialize_environment()

    if not HAMILTONIAN_FILE_PATH.exists():
        msg = (
            f"Файл [bold]{HAMILTONIAN_FILE_PATH}[/] не найден!\n"
            "Убедитесь, что рядом с EXE есть папка [bold]params[/] с файлом [bold]hamiltonian_operators.txt[/]."
        )
        console_and_print(console, Panel(msg, border_style="red"))
        return

    try:
        pauli_operators, pauli_strings = read_hamiltonian_data(HAMILTONIAN_FILE_PATH)
        print_hamiltonian(console, pauli_operators)
        print_pauli_table(console, pauli_operators)
        print_composition_table(console, pauli_compose, pauli_strings)
    except FileNotFoundError:
        console_and_print(console, Panel(f"[red]Файл {HAMILTONIAN_FILE_PATH} не найден[/red]", border_style="red"))
        return

    if len(pauli_operators) < 2:
        console_and_print(console, Panel("[red]Требуется минимум 2 оператора Паули[/red]", border_style="red"))
        return

    # Параметры алгоритма отжига
    SA_PARAMS = {
        "initial_temp": 100.0,
        "cooling_rate": 0.95,
        "min_temp": 1e-3,
        "num_iterations_per_temp": 100,
        "step_size": 0.1,
    }

    # Рассчитываем общее количество шагов
    thermalization_steps = int(SA_PARAMS["num_iterations_per_temp"] * 0.2)
    temp_steps = calculate_temp_steps(
        SA_PARAMS["initial_temp"], 
        SA_PARAMS["cooling_rate"], 
        SA_PARAMS["min_temp"]
    )
    steps_per_m = temp_steps * (thermalization_steps + SA_PARAMS["num_iterations_per_temp"])
    total_steps = steps_per_m * (len(pauli_operators) - 1)

    best_energy = float("inf")
    best_result = None
    all_results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("[cyan]Отжиг...", total=total_steps)

        for m in range(2, len(pauli_operators) + 1):
            current_ops = pauli_operators[:m]
            initial_theta = generate_shifted_theta(current_ops)

            optimized_theta, energy = simulated_annealing(
                initial_theta=initial_theta,
                pauli_operators=current_ops,
                progress=progress,
                task=task,
                **SA_PARAMS
            )

            all_results.append({
                "m": m,
                "theta": optimized_theta,
                "energy": energy,
                "operators": current_ops
            })

            if energy < best_energy:
                best_energy = energy
                best_result = all_results[-1]

    # Вывод результатов
    if best_result is None:
        console_and_print(console, Panel("[red]Не удалось найти решение[/red]", border_style="red"))
        return

    _, ansatz_symbolic, ansatz_numeric = calculate_ansatz(
        best_result["theta"],
        best_result["operators"]
    )

    console_and_print(console, Panel(ansatz_symbolic,
        title="[bold]Символьное представление анзаца[/]", border_style="green"))

    console_and_print(console, Panel(ansatz_numeric,
        title="[bold]Численное представление анзаца[/]", border_style="purple"))

    console_and_print(console, Panel(f"{best_result['energy']:.6f}",
        title="[bold]Энергия (<0|U†HU|0> для состояния |0...0>)[/]", border_style="green"))

    input('Нажмите Enter для выхода...')


if __name__ == "__main__":
    main()
