using Microsoft.Extensions.Configuration;
using System;

namespace Quarterback
{
    public class GreetingService : IGreetingService
    {
        private readonly IConfiguration _config;

        public GreetingService(IConfiguration config)
        {
            _config = config;
        }
        public void Run()
        {
            for (int i = 0; i < _config.GetValue<int>("LoopTimes"); i++)
            {
                Console.WriteLine($"We are { i } ");
            }
        }
    }
}
