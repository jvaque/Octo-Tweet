using Microsoft.Extensions.Configuration;
using Octo_Tweet.Library.Api;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace Quarterback
{
    public class StartService : IStartService
    {
        private readonly IConfiguration _config;
        private readonly IOctopusHelper _octopusHelper;

        public StartService(IConfiguration config, IOctopusHelper octopusHelper)
        {
            _config = config;
            _octopusHelper = octopusHelper;
        }

        public async Task Run()
        {
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            var electricityUse = await _octopusHelper.GetElectricityConsumption(electricityMPAN, electricitySerialNumber);

            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            var gasUse = await _octopusHelper.GetGasConsumption(gasMPAN, gasSerialNumber);
        }
    }
}
