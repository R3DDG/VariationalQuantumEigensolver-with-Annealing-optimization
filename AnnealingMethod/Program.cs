using System;
using System.Collections.Generic;

class Program
{
	static void Main()
	{
		Console.OutputEncoding = System.Text.Encoding.UTF8;

		List<Term> hamiltonianTerms = new List<Term>();

		Console.WriteLine("Введите количество слагаемых в гамильтониане:");
		string? ts = Console.ReadLine() ?? "3";
		int termsCount = int.Parse(ts);

		for (int i = 0; i < termsCount; i++)
		{
			Console.WriteLine($"Введите коэффициент для слагаемого {i + 1}:");
			string? c = Console.ReadLine() ?? "0";
			int coefficient = int.Parse(c);

			Console.WriteLine($"Введите индекс оператора Паули для слагаемого {i + 1}:");
			string? ind = Console.ReadLine() ?? "0";
			int index = int.Parse(ind);

			hamiltonianTerms.Add(new Term(coefficient, index));
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

		Console.WriteLine($"Введенный гамильтониан: {hamiltonianString}");
	}
}

class Term
{
	public int Coefficient { get; }
	public int Index { get; }

	public Term(int coefficient, int index)
	{
		Coefficient = coefficient;
		Index = index;
	}

	public override string ToString()
	{
		return Coefficient != 1 ? $"{Coefficient}*σ_{Index}" : $"σ_{Index}";
	}
}
