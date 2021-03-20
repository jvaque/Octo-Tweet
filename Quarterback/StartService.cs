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

        public async Task Run(string[] args)
        {
            //Modify program to take args from program start so with a simple flag you can make a call to get all the 
            // history or to manually get values from a specific date (just go wild)
            // remember to make changes to the debug propperties to propperly test this changes.
            //Look into how to properly code for modifiers in a console application.
            if (args[0] == "-a")
            {
                // Retrieve and save all the history from Electricity & Gas
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
            else
            {
                // Retrieve and save all the new infromation from Electricity & Gas
                // Electricity
                List<ElectricityModel> tempNameElectricityNew = await NewHistoryElectricity();

                if (tempNameElectricityNew.Count > 0)
                {
                    await _electricity.SaveListElectricityAsync(tempNameElectricityNew);
                }

                // Gas
                List<GasModel> tempNameGasNew = await NewHistoryGas();

                if (tempNameGasNew.Count > 0)
                {
                    await _gas.SaveListGasAsync(tempNameGasNew);
                }
            }
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

        private async Task<List<ElectricityModel>> NewHistoryElectricity()
        {
            // Retrieve config values
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            // Retrieve latest record from database
            ElectricityModel lastRecordElectricity = await _electricity.RetrieveLastRecordElectricityAsync();

            // Variables
            List<ElectricityModel> returnList = new List<ElectricityModel>();
            int page = 1;
            int useCount = 0;

            while (true)
            {
                // Get a page of values
                ApiElectricityModel temp = await _octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber);

                if (useCount == 0)
                {
                    useCount = temp.Count;
                }
                else if (useCount != temp.Count)
                {
                    // Throw an error if the ammount of records get changed as the program is making subsequent calls
                    // Look if there is a more gracefull way of handling this error in the future
                    throw new Exception();
                }

                // Parse from ApiElectricityModel to List<ElectricityModel>
                List<ElectricityModel> tempList = MapApiElectricityToDatabase(temp);

                // Look at each record and determine if the last record in the database has been reached
                foreach (var item in tempList)
                {
                    // TODO: look at a way to incorporate a way to determine if two instances of a class hold the same values determining them as "equal" 
                    //  even if they are different instances of a class.
                    bool tempBoolTest = item.Electricity_consumption == lastRecordElectricity.Electricity_consumption &
                                        item.Electricity_interval_start_datetime == lastRecordElectricity.Electricity_interval_start_datetime &
                                        item.Electricity_interval_start_offset == lastRecordElectricity.Electricity_interval_start_offset &
                                        item.Electricity_interval_end_datetime == lastRecordElectricity.Electricity_interval_end_datetime &
                                        item.Electricity_interval_end_offset == lastRecordElectricity.Electricity_interval_end_offset;

                    // Record match found
                    if (tempBoolTest)
                    {
                        return returnList;
                    }
                    // Record not found
                    else
                    {
                        returnList.Add(item);
                    }
                }

                page++;

            }
        }

        private async Task<List<GasModel>> NewHistoryGas()
        {
            // Retrieve config values
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            // Retrieve latest record from database
            GasModel lastRecordGas = await _gas.RetrieveLastRecordGasAsync();

            // Variables
            List<GasModel> returnList = new List<GasModel>();
            int page = 1;
            int useCount = 0;

            while (true)
            {
                // Get a page of values
                ApiGasModel temp = await _octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber);

                if (useCount == 0)
                {
                    useCount = temp.Count;
                }
                else if (useCount != temp.Count)
                {
                    // Throw an error if the ammount of records get changed as the program is making subsequent calls
                    // Look if there is a more gracefull way of handling this error in the future
                    throw new Exception();
                }

                // Parse from ApiGasModel to List<GasModel>
                List<GasModel> tempList = MapApiGasToDatabase(temp);

                // Look at each record and determine if the last record in the database has been reached
                foreach (var item in tempList)
                {
                    // TODO: look at a way to incorporate a way to determine if two instances of a class hold the same values determining them as "equal" 
                    //  even if they are different instances of a class.
                    bool tempBoolTest = item.Gas_consumption == lastRecordGas.Gas_consumption &
                                        item.Gas_interval_start_datetime == lastRecordGas.Gas_interval_start_datetime &
                                        item.Gas_interval_start_offset == lastRecordGas.Gas_interval_start_offset &
                                        item.Gas_interval_end_datetime == lastRecordGas.Gas_interval_end_datetime &
                                        item.Gas_interval_end_offset == lastRecordGas.Gas_interval_end_offset;

                    // Record match found
                    if (tempBoolTest)
                    {
                        return returnList;
                    }
                    // Record not found
                    else
                    {
                        returnList.Add(item);
                    }
                }

                page++;

            }
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
