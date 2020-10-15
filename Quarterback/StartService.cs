using Microsoft.Extensions.Configuration;
using Octo_Tweet.Library.Api;
using Octo_Tweet.Library.Models;
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

            ElectricityModel electricityUse = await _octopusElectricityHelper.GetConsumption(electricityMPAN, electricitySerialNumber);

            double electricityPages = Math.Ceiling(electricityUse.Count / 100d);

            List<ConsumptionDetail> allHistoryElectricityUse = new List<ConsumptionDetail>();
            for (int page = 1; page < (electricityPages+1); page++)
            {
                allHistoryElectricityUse.AddRange((await _octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber)).Results);
            }


            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            GasModel gasUse = await _octopusGasHelper.GetConsumption(gasMPAN, gasSerialNumber);

            double gasPages = Math.Ceiling(gasUse.Count / 100d);

            List<ConsumptionDetail> allHistoryGasUse = new List<ConsumptionDetail>();
            for (int page = 1; page < (gasPages + 1); page++)
            {
                allHistoryGasUse.AddRange((await _octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber)).Results);
            }
        }

        // Todo make calls to the electricity and gas endpoint in their distinct async calls for better performance
        //private async Task<List<ConsumptionDetail>> Electricity()
        //{

        //}
    }
}
