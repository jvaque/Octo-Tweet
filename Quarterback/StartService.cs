using Microsoft.Extensions.Configuration;
using Octo_Tweet.Data.Libary.DataAccess;
using Octo_Tweet.Data.Libary.Models;
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
        private readonly IElectricity _electricity;
        private readonly IGas _gas;

        public StartService(
            IConfiguration config, 
            IOctopusElectricityHelper octopusElectricityHelper, 
            IOctopusGasHelper octopusGasHelper,
            IElectricity electricity,
            IGas gas
            )
        {
            _config = config;
            _octopusElectricityHelper = octopusElectricityHelper;
            _octopusGasHelper = octopusGasHelper;
            _electricity = electricity;
            _gas = gas;
        }

        public async Task Run()
        {
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            ApiElectricityModel electricityUse = await _octopusElectricityHelper.GetConsumption(electricityMPAN, electricitySerialNumber);

            List<ApiElectricityModel> allHistoryElectricityUse = await AllHistoryElectricity(electricityUse.Count);

            List<List<ElectricityModel>> veryBadNameElectricity = new List<List<ElectricityModel>>();
            foreach (var item in allHistoryElectricityUse)
            {
                veryBadNameElectricity.Add(MapApiElectricityToDatabase(item));
            }

            List<Task> tasks = new List<Task>();
            foreach (var item in veryBadNameElectricity)
            {
                tasks.Add(_electricity.SaveListElectricityAsync(item));
            }

            await Task.WhenAll(tasks);


            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            ApiGasModel gasUse = await _octopusGasHelper.GetConsumption(gasMPAN, gasSerialNumber);

            List<ApiGasModel> allHistoryGasUse = await AllHistoryGas(gasUse.Count);

            List<List<GasModel>> veryBadNameGas = new List<List<GasModel>>();
            foreach (var item in allHistoryGasUse)
            {
                veryBadNameGas.Add(MapApiGasToDatabase(item));
            }

            tasks = new List<Task>();
            foreach (var item in veryBadNameGas)
            {
                tasks.Add(_gas.SaveListGasAsync(item));
            }

            await Task.WhenAll(tasks);

        }

        private List<ElectricityModel> MapApiElectricityToDatabase(ApiElectricityModel apiElectricityModel)
        {
            List<ElectricityModel> output = new List<ElectricityModel>();
            foreach (var item in apiElectricityModel.Results)
            {
                output.Add(new ElectricityModel()
                {
                    Electricity_consumption = item.Consumption,
                    Electricity_interval_start_datetime = item.Interval_start.DateTime,
                    Electricity_interval_start_offset = item.Interval_start.Offset,
                    Electricity_interval_end_datetime = item.Interval_end.DateTime,
                    Electricity_interval_end_offset = item.Interval_end.Offset
                });
            }
            
            return output;
        }
        
        private List<GasModel> MapApiGasToDatabase(ApiGasModel apiGasModel)
        {
            List<GasModel> output = new List<GasModel>();
            foreach (var item in apiGasModel.Results)
            {
                output.Add(new GasModel()
                {
                    Gas_consumption = item.Consumption,
                    Gas_interval_start_datetime = item.Interval_start.DateTime,
                    Gas_interval_start_offset = item.Interval_start.Offset,
                    Gas_interval_end_datetime = item.Interval_end.DateTime,
                    Gas_interval_end_offset = item.Interval_end.Offset
                });
            }
            
            return output;
        }

        private async Task<List<ApiElectricityModel>> AllHistoryElectricity(double useCount)
        {
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            double electricityPages = Math.Ceiling(useCount / 100d);

            List<ApiElectricityModel> electricityHistory = new List<ApiElectricityModel>();
            List<Task<ApiElectricityModel>> tasks = new List<Task<ApiElectricityModel>>();

            for (int page = 1; page < (electricityPages + 1); page++)
            {
                tasks.Add(_octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber));
            }

            var results = await Task.WhenAll(tasks);
            foreach (var item in results)
            {
                electricityHistory.Add(item);
            }

            return electricityHistory;
        }

        private async Task<List<ApiGasModel>> AllHistoryGas(double useCount)
        {
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            double gasPages = Math.Ceiling(useCount / 100d);

            List<ApiGasModel> gasHistory = new List<ApiGasModel>();
            List<Task<ApiGasModel>> task = new List<Task<ApiGasModel>>();

            for (int page = 1; page < (gasPages + 1); page++)
            {
                task.Add(_octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber));
            }

            var results = await Task.WhenAll(task);
            foreach (var item in results)
            {
                gasHistory.Add(item);
            }

            return gasHistory;
        }
    }
}
