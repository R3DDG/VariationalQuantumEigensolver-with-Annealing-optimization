using System;
	
class Program
{													
	static void Main()
	{
	// ###############  Входные данные  ##################
		
		//n - число городов, N - число итераций
		//E - энергия, целевая функция (длина пути)
		//T - температура,  tau - шаг уменьшения температуры
		int n = 10, N = 1000; 
		double E = 0.0, T = 30.0, tau = 0.02;
		
		//C - конфигурация (перестановка набора 012...n-1)
		int[] C = new int[n];
		//Определим начальную конфигурацию
		for(int i=0; i<n; i++) C[i] = i;
		
		//L[i,j] - расстояние между городами i и j
		double[ , ] L = new double[n,n];
		
		//( P[0,k], P[1,k] ) - координаты (x,y) города k
		double[ , ] P =  
		{{-2.0, -3.0, 0.0, 3.4, 1.8, -1.0, -1.6, 0.3, 1.5, 0.9},
		{-1.4, 1.2, 4.0, 0.8, -1.1, -0.3, 0.6, 1.3, 0.5, -0.3}};
		
		//Заполняем матрицу расстояний L{i,j}
		for(int i=0; i<n; i++) 
		{ 
			for(int j=0; j<n; j++)
			{   
				L[i,j] = Math.Sqrt(
				(P[0,i]-P[0,j])*(P[0,i]-P[0,j]) + 
				(P[1,i]-P[1,j])*(P[1,i]-P[1,j]) ); 
			}
		}
		
		//Печать начальной конфигурации
		Console.WriteLine("start config");
		printC(n, C); //Метод (ниже) для печати массива C
		
		for(int k=1; k<n; k++) E = E + L[C[k-1], C[k]];
		Console.WriteLine("   E = " + E);
		E = 0.0;
		
		
	// #############  Выполнение программы  ################
				
		Annealing ann = new Annealing();
		
				
		//Выполняем основной метод
		ann.Boltzmann(n, N, ref C, L, ref E, ref T, tau);
		Console.WriteLine("result config");
		printC(n, C);
		Console.WriteLine("   E = " + E + ", T = " + T);
		Console.WriteLine();
		Console.ReadKey();		
	}
	
	//Вспомогательный метод для печати массива конфигурации
	static public void printC(int n, int[] C)
	{
		for (int i = 0; i < n; i++)
		Console.WriteLine(" " + C[i]);
	}
}


//Реализация алгоритма методами Boltzmann, trans, path
class Annealing
{
	Random rnd = new Random();
	
	//Метод-функция копирует массив C в массив copy
	public int[] copy(int n, int[] C)
	{
		int[] copyC = new int[n];
		for(int i=0; i<n; i++) copyC[i] = C[i];
		return copyC;
	}

	public void Boltzmann(int n, int N, ref int[] C, double[,] L, 
		ref double E, ref double T, double tau)
	{		
		int[] newC = new int[n]; newC = copy(n, C);
		int[] minC = new int[n]; minC = copy(n, C);
		
		
		double Enew, Eold, Emin, delta;
		
		Eold = path(n, C, L);
		Emin = Eold;
		
		for (int i = 0; i < N; i++)	
		{
			//Изменяем конфигурацию
			trans(n, ref newC, ref rnd);
			
			//Вычисляем новую длину пути
			Enew = path(n, newC, L);
			delta = Math.Exp((Eold - Enew)/T);
			
			if(rnd.NextDouble() < delta)
			{
				Eold = Enew;
				C = copy(n, newC);
				if(Enew < Emin)
				{	
					Emin = Enew; minC = copy(n, newC);
				}
			}
			 
			//Уменьшаем температуру
			T = T - tau;
		}
		
		C = copy(n, minC);
		E = Emin;
	}
	
	//Метод trans изменяет конфигурацию (путь)
	//переставляя местами два города
	static public void trans(int n, ref int[] C, ref Random rnd)//, ref Random rnd
	{
		int i = rnd.Next(n-1) + 1;
		int j = rnd.Next(n-1) + 1;
		int k = C[i];
		C[i] = C[j];
		C[j] = k;
	}
	
	//Метод path вычисляет длину пути
	static public double path(int n, int[] C, double[,] L)
	{
		double S = 0;
		for(int k=1; k<n; k++) S = S + L[C[k-1], C[k]];
		return S;
	}
} 

