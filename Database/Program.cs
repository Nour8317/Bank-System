using System;
using Database.SystemManager;
namespace Database
{
    public class Program
    {
        public static void Main(string[] args)
        {
            Manager M = new Manager();
            M.Run();
        }
    }
}