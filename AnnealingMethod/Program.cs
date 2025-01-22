using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;

class Program
{
	static void Main()
	{
		Console.OutputEncoding = System.Text.Encoding.UTF8;

		List<Term> hamiltonianTerms = new List<Term>();

		// Путь к файлам
		string hamiltonianFilePath = "hamiltonian_operators.txt";
		string coefficientsFilePath = "coefficients.txt";

		// Чтение данных из файла гамильтониана
		string[] hamiltonianLines = File.ReadAllLines(hamiltonianFilePath);
		int termsCount = hamiltonianLines.Length;

		for (int i = 0; i < termsCount; i++)
		{
			string line = hamiltonianLines[i];
			string[] parts = line.Split(' ');

			if (parts.Length != 3)
			{
				Console.WriteLine("Неверный формат строки: " + line);
				continue;
			}

			double realPart = double.Parse(parts[0], CultureInfo.InvariantCulture);
			double imaginaryPart = double.Parse(parts[1], CultureInfo.InvariantCulture);
			int index = int.Parse(parts[2]);

			ComplexNumber coefficient = new ComplexNumber(realPart, imaginaryPart);
			if (coefficient.Real != 0 || coefficient.Imaginary != 0)
			{
				hamiltonianTerms.Add(new Term(coefficient, index));
			}
		}

		string hamiltonianString = "H = ";
		for (int i = 0; i < hamiltonianTerms.Count; i++)
		{
			Term term = hamiltonianTerms[i];
			hamiltonianString += term.ToString();

			if (i < hamiltonianTerms.Count - 1)
			{
				hamiltonianString += " + ";
			}
		}

		// Вывод введенного гамильтониана
		Console.WriteLine($"Введенный гамильтониан: {hamiltonianString}");

		// Пустая строка
		Console.WriteLine();

		// Вывод термов гамильтониана
		PrintHamiltonianTerms(hamiltonianTerms);

		// Генерация случайных чисел
		Console.WriteLine("\nСлучайные числа θ_i:");
		double[] theta = GenerateRandomTheta(5); // Например, 5 случайных чисел
		foreach (var t in theta)
		{
			Console.WriteLine(t.ToString(CultureInfo.InvariantCulture));
		}

		// Чтение коэффициентов из файла
		double[] coefficients = ReadCoefficientsFromFile(coefficientsFilePath);
		if (coefficients.Length != theta.Length)
		{
			Console.WriteLine("Ошибка: количество коэффициентов не совпадает с количеством переменных θ.");
			return;
		}

		// Вычисление целевой функции
		double functionValue = ComputeObjectiveFunction(theta, coefficients);
		Console.WriteLine($"\nЗначение целевой функции: {functionValue.ToString(CultureInfo.InvariantCulture)}");
	}

	static void PrintHamiltonianTerms(List<Term> terms)
	{
		Console.WriteLine("Термы гамильтониана:");
		foreach (var term in terms)
		{
			Console.WriteLine($"Коэффициент - {term.Coefficient}, индекс - {term.Index}");
		}
	}

	static double[] GenerateRandomTheta(int m)
	{
		Random random = new Random();
		double[] theta = new double[m];
		for (int i = 0; i < m; i++)
		{
			theta[i] = random.NextDouble(); // Генерация случайного числа от 0 до 1
		}
		return theta;
	}

	static double[] ReadCoefficientsFromFile(string filePath)
	{
		string[] coefficientLines = File.ReadAllLines(filePath);
		double[] coefficients = new double[coefficientLines.Length];
		for (int i = 0; i < coefficientLines.Length; i++)
		{
			coefficients[i] = double.Parse(coefficientLines[i], CultureInfo.InvariantCulture);
		}
		return coefficients;
	}

	static double ComputeObjectiveFunction(double[] theta, double[] coefficients)
	{
		double sum = 0;
		for (int i = 0; i < theta.Length; i++)
		{
			sum += theta[i] * coefficients[i];
		}
		return sum; // Простая линейная комбинация
	}
}

class Term
{
	public ComplexNumber Coefficient { get; }
	public int Index { get; }

	public Term(ComplexNumber coefficient, int index)
	{
		Coefficient = coefficient;
		Index = index;
	}

	public override string ToString()
	{
		return Coefficient.ToString() + $"*σ_{Index}";
	}
}

public class ComplexNumber
{
	public double Real { get; }
	public double Imaginary { get; }

	public ComplexNumber(double real, double imaginary)
	{
		Real = real;
		Imaginary = imaginary;
	}

	public override string ToString()
	{
		string realPart = Real != 0 ? Real.ToString(CultureInfo.InvariantCulture) : "";

		string imaginaryPart = Imaginary switch
		{
			0 => "",
			1 => "i",
			-1 => "-i",
			_ => $"{Imaginary.ToString(CultureInfo.InvariantCulture)}i"
		};

		if (string.IsNullOrEmpty(realPart))
			return imaginaryPart;

		if (string.IsNullOrEmpty(imaginaryPart))
			return realPart;

		return Imaginary > 0
			? $"{realPart} + {imaginaryPart}"
			: $"{realPart} - {imaginaryPart.Substring(1)}";
	}
}
