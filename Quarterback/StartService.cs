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
            // Electricity
            List<List<ElectricityModel>> allHistoryElectricityUse = await AllHistoryElectricity();

            List<Task> tasks = new List<Task>();
            foreach (var item in allHistoryElectricityUse)
            {
                tasks.Add(_electricity.SaveListElectricityAsync(item));
            }

            await Task.WhenAll(tasks);

            // Gas
            List<List<GasModel>> allHistoryGasUse = await AllHistoryGas();

            tasks = new List<Task>();
            foreach (var item in allHistoryGasUse)
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

        private async Task<List<List<ElectricityModel>>> AllHistoryElectricity()
        {
            // Retrieve config values
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            // Call api to retrieve count or records to retrieve
            ApiElectricityModel tempUse = await _octopusElectricityHelper.GetConsumption(electricityMPAN, electricitySerialNumber);

            double electricityPages = Math.Ceiling(tempUse.Count / 100d);

            List<List<ElectricityModel>> electricityHistory = new List<List<ElectricityModel>>();
            List<Task<ApiElectricityModel>> tasks = new List<Task<ApiElectricityModel>>();

            for (int page = 1; page < (electricityPages + 1); page++)
            {
                tasks.Add(_octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber));
            }

            var results = await Task.WhenAll(tasks);
            int countOfRetrievedRecords = 0;
            foreach (var item in results)
            {
                List<ElectricityModel> tempList = MapApiElectricityToDatabase(item);
                countOfRetrievedRecords += tempList.Count;
                electricityHistory.Add(tempList);
            }

            if (tempUse.Count == countOfRetrievedRecords)
            {
                return electricityHistory;
            }
            else
            {
                // TODO: Find a more elegant way to handle the error
                throw new Exception();
            }

        }

        private async Task<List<List<GasModel>>> AllHistoryGas()
        {
            // Retrieve config values
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            // Call api to retrieve count or records to retrieve
            ApiGasModel tempUse = await _octopusGasHelper.GetConsumption(gasMPAN, gasSerialNumber);

            double gasPages = Math.Ceiling(tempUse.Count / 100d);

            List<List<GasModel>> gasHistory = new List<List<GasModel>>();
            List<Task<ApiGasModel>> task = new List<Task<ApiGasModel>>();

            for (int page = 1; page < (gasPages + 1); page++)
            {
                task.Add(_octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber));
            }

            var results = await Task.WhenAll(task);
            int countOfRetrievedRecords = 0;
            foreach (var item in results)
            {
                List<GasModel> tempList = MapApiGasToDatabase(item);
                countOfRetrievedRecords += tempList.Count;
                gasHistory.Add(tempList);
            }

            if (tempUse.Count == countOfRetrievedRecords)
            {
                return gasHistory;
            }
            else
            {
                // TODO: Find a more elegant way to handle the error
                throw new Exception();
            }
        }
    }
}
