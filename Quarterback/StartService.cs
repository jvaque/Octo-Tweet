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
        private readonly IOctopusElectricityHelper _octopusElectricityHelper;
        private readonly IOctopusGasHelper _octopusGasHelper;

        public StartService(IConfiguration config, IOctopusElectricityHelper octopusElectricityHelper, IOctopusGasHelper octopusGasHelper)
        {
            _config = config;
            _octopusElectricityHelper = octopusElectricityHelper;
            _octopusGasHelper = octopusGasHelper;
        }

        public async Task Run()
        {
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            var electricityUse = await _octopusElectricityHelper.GetConsumption(electricityMPAN, electricitySerialNumber);

            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            var gasUse = await _octopusGasHelper.GetConsumption(gasMPAN, gasSerialNumber);
        }
    }
}
