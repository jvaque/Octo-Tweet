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

            List<ConsumptionDetail> allHistoryElectricityUse = await AllHistoryElectricity(electricityUse.Count);

            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            GasModel gasUse = await _octopusGasHelper.GetConsumption(gasMPAN, gasSerialNumber);

            List<ConsumptionDetail> allHistoryGasUse = await AllHistoryGas(gasUse.Count);

        }

        private async Task<List<ConsumptionDetail>> AllHistoryElectricity(double useCount)
        {
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            double electricityPages = Math.Ceiling(useCount / 100d);

            List<ConsumptionDetail> electricityHistory = new List<ConsumptionDetail>();
            List<Task<ElectricityModel>> tasks = new List<Task<ElectricityModel>>();

            for (int page = 1; page < (electricityPages + 1); page++)
            {
                tasks.Add(_octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber));
            }

            var results = await Task.WhenAll(tasks);
            foreach (var item in results)
            {
                electricityHistory.AddRange(item.Results);
            }

            return electricityHistory;
        }

        private async Task<List<ConsumptionDetail>> AllHistoryGas(double useCount)
        {
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            double gasPages = Math.Ceiling(useCount / 100d);

            List<ConsumptionDetail> gasHistory = new List<ConsumptionDetail>();
            List<Task<GasModel>> task = new List<Task<GasModel>>();

            for (int page = 1; page < (gasPages + 1); page++)
            {
                task.Add(_octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber));
            }

            var results = await Task.WhenAll(task);
            foreach (var item in results)
            {
                gasHistory.AddRange(item.Results);
            }

            return gasHistory;
        }
    }
}
