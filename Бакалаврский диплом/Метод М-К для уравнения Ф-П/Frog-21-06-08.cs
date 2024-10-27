using System;
using System.Text;
using System.IO;


namespace RandomWalks
{
    class Program
    {
        static void Main(string[] args)
        {
			Console.Write("Введите число шагов n = ");
			int n = Convert.ToInt32(Console.ReadLine());
			Console.WriteLine ();
			Console.Write("Введите вероятность перехода направо p = ");
			double p = Convert.ToDouble(Console.ReadLine());//Если p=0.75, то k=1, D=0.25
			Console.WriteLine ();
			
			double Xmax = 16.0, T = 8.0, h, tau, k, D;
			h = Xmax/n; tau = T/n; k = Xmax/T*(2*p-1); D = h*Xmax/T*(2*p*p-2*p+1);
			
			int dim = 2*n+1, N = 100000000, scale;
			scale = 2*Convert.ToInt32(Convert.ToDouble(n)/Xmax+0.01);
			
			Console.WriteLine
			(" h={0,5:F3}, tau={1,5:F3}, scale={2,2}, k={3,3:F2}, D={4,3:F2}", h,tau,scale,k,D);
			Console.WriteLine();
			
			string path1 = @"D:\Library\CSharp\CSC\Model.txt";
			string path2 = @"D:\Library\CSharp\CSC\Exact.txt";
			string format = " {0,4} {1,12:F9}";
			
            Frog frog = new Frog(n, p, N);

			//Запись значений точного решения уравнения Фоккера-Планка в массив FP
			
			double[]FP = new double[dim];
			for (int m = 0; m < dim; m++)
            {
                double x = (m-n)*h - k*T; 
                FP[m] = 1 / Math.Sqrt(4*Math.PI*D*T) * Math.Exp(-x*x/(4*D*T));
            }
			
			//Вывод результатов моделирования и точного решения из массивов P и FP
			//на экран и в файлы Model.txt и Exact.txt

			for (int i = 0; i < dim; i++) 
			{
				if (i % scale == 0) 
				Console.WriteLine(" {0,4} {1,12:F9} {2,12:F9}", h*(i-n), frog.P[i], FP[i]);
			}
			
			using (StreamWriter MC = new StreamWriter(path1, false, Encoding.Default))
			{				
				for (int i = 0; i < dim; i++) 
				{
					if (i % scale == 0)MC.WriteLine(format, h*(i - n), 1.6*frog.P[i]);
				}
			}
			
			using (StreamWriter E = new StreamWriter(path2, false, Encoding.Default))
			{				
				for (int i = 0; i < dim; i++) 
				{
					if (i % scale == 0) E.WriteLine(format, h*(i - n), FP[i]);
				}
			}
			
            Console.ReadKey();
        }
    }
	
	class Frog
	{
		public int n, N;
		public double p;
		public double[] P;		
		
		public Frog(int n, double p, int N)
		{
			this.n = n; this.p = p; this.N = N;
			int dim = 2*n+1;
			this.P = new double[dim];
			
			Random rnd =  new Random();

			for(int i = 0; i < N; i++)
            {
                int k = n;
                for(int j = 0; j < n; j++)
                {
                    if (rnd.NextDouble() < p){k = k+1;} 
					else{k = k-1;}
                }
                P[k] += 1;
            }
			
			for(int i = 0; i < dim; i++) P[i] = P[i] / N;
		}
	}
}
