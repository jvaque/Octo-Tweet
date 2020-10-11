using Octo_Tweet.Library.Api;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace Quarterback
{
    public class StartService : IStartService
    {
        private readonly IOctopusHelper _octopusHelper;

        public StartService(IOctopusHelper octopusHelper)
        {
            _octopusHelper = octopusHelper;
        }

        public async Task Run()
        {
            Console.WriteLine("Hello from the start of the program, Delete this later");

            var electricityUse = await _octopusHelper.GetElectricityConsumption();
            var gasUse = await _octopusHelper.GetGasConsumption();
        }
    }
}
