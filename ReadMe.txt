Модифицированная версия программы автора "KoTuK2306". Ключевые изменения:
1. Удобный ручной ввод анзаца;
2. Оптимизация вычислений и самой программы.

Программа реализует вариационный квантовый алгоритм с использованием метода отжига для оптимизации квантовых состояний. Для реализации метода отжига в качестве оптимизатора, использована библиотека Sci-Py. Остальные вычислительные модули взяты из источника и были немного оптимизированы.

Гамильтониан задается в папке params, файл hamiltonian_operators.txt.
При запуске программы, сначала необходимо ввести количество параметров для построения анзаца, затем для каждого параметра вводим оператор Паули. После этого, необходимо подождать некоторое время, пока производятся расчеты.
В программе используется рандомизация theta с подмешиванием шума Гаусса для каждого нового параметра theta (имитация шума квантового компьютера).
Так как в вычислениях присутствует вероятность, рекомендуется производить запуск программы несколько раз и выбрать наименьшее значение энергии из полученных.
В программе предусмотрен промежуточный вывод для отслеживания динамики изменения энергии, а также отображение импортированных/введенных данных.

Основной алгоритм программы:
1. Предложение ввода анзаца;
2. Чтение файла с описанием гамильтониана;
3. Генерация случайным образом начальных параметров theta с подмешиванием шума для введенного анзаца;
4. Запуск алгоритма вычислений;
5. Вывод результатов.

Тестирование программы выполнено на гамильтониане водорода (записан в файле с описанием гамильтониана) и четырехпараметровом анзаце, описанном в файле "Ввод анзаца. txt". Параметры отжига определены как: начальная температура 50, множитель охлаждения 0.98, минимальная температура 1e-6 (1*10^-6), 38 итераций на температуру. В результате, как минимум в одном из пяти пробных запусков программы, было получено эталонное значение энергии гамильтониана водорода равное -1.136.




A modified version of the author's program "KoTuK2306". Key changes:
1. Convenient manual insertion of the ansatz;
2. Optimization of calculations and the program itself.

The program implements a variational quantum algorithm using the annealing method to optimize quantum states. To implement the annealing method as an optimizer, the Sci-Py library was used. The rest of the computing modules are taken from the source and have been slightly optimized.

The Hamiltonian is set in the params folder, the file hamiltonian_operators.txt .
When starting the program, you need to enter the number of parameters for constructing the ansatz, then enter the Pauli operator for each parameter. After that, it is necessary to wait for some time while calculations are being made.
The program uses theta randomization with Gauss noise mixing for each new theta parameter (simulating the noise of a quantum computer).
Since there is a probability in the calculations, it is recommended to run the program several times and select the lowest energy value from the received ones.
The program provides an intermediate output for tracking the dynamics of energy changes, as well as displaying imported/entered data.

The main algorithm of the program is:
1. The suggestion of entering an ansatz;
2. Reading the file with the description of the Hamiltonian;
3. Random generation of initial theta parameters with noise mixing for the entered ansatz;
4. Running the calculation algorithm;
5. Output of the results.

The program was tested on the hydrogen Hamiltonian (written in the file with the description of the Hamiltonian) and the four-parameter ansatz described in the file "Entering the ansatz. txt". The annealing parameters are defined as: initial temperature 50, cooling multiplier 0.98, minimum temperature 1e-6 (1*10^-6), 38 iterations on the temperature. As a result, in at least one of the five trial runs of the program, a reference value of the energy of the hydrogen Hamiltonian equal to -1.136 was obtained.
