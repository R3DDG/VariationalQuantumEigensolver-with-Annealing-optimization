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

		// Путь к файлу
		string filePath = "input.txt";

		// Чтение данных из файла
		string[] lines = File.ReadAllLines(filePath);
		int termsCount = lines.Length;

		for (int i = 0; i < termsCount; i++)
		{
			string line = lines[i];
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
	}

	static void PrintHamiltonianTerms(List<Term> terms)
	{
		Console.WriteLine("Термы гамильтониана:");
		foreach (var term in terms)
		{
			Console.WriteLine($"Коэффициент - {term.Coefficient}, индекс - {term.Index}");
		}
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
		string realPart = Real != 0 ? Real.ToString() : "";

		string imaginaryPart = Imaginary switch
		{
			0 => "",
			1 => "i",
			-1 => "-i",
			_ => $"{Imaginary}i"
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
