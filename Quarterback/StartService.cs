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
        private readonly IDataSources _dataSources;
        private readonly IDataValues _dataValues;

        public StartService(
            IConfiguration config, 
            IOctopusElectricityHelper octopusElectricityHelper, 
            IOctopusGasHelper octopusGasHelper,
            IDataSources dataSources,
            IDataValues dataValues
            )
        {
            _config = config;
            _octopusElectricityHelper = octopusElectricityHelper;
            _octopusGasHelper = octopusGasHelper;
            _dataSources = dataSources;
            _dataValues = dataValues;
        }

        public async Task Run(string[] args)
        {
            //Modify program to take args from program start so with a simple flag you can make a call to get all the 
            // history or to manually get values from a specific date (just go wild)
            // remember to make changes to the debug propperties to propperly test this changes.
            //Look into how to properly code for modifiers in a console application.
            if (args != null && args.Length > 0)
            {
                if (args[0] == "-a" || args[0] == "--all")
                {
                    // Retrieve and save all the history from Electricity & Gas
                    // Electricity
                    List<List<DataValuesModel>> allHistoryElectricityUse = await AllHistoryElectricity();

                    List<Task> tasks = new List<Task>();
                    foreach (var item in allHistoryElectricityUse)
                    {
                        tasks.Add(_dataValues.SaveListDataValuesAsync(item));
                    }

                    await Task.WhenAll(tasks);

                    // Gas
                    List<List<DataValuesModel>> allHistoryGasUse = await AllHistoryGas();

                    tasks = new List<Task>();
                    foreach (var item in allHistoryGasUse)
                    {
                        tasks.Add(_dataValues.SaveListDataValuesAsync(item));
                    }

                    await Task.WhenAll(tasks);
                }
                else
                {
                    Console.WriteLine($"Unrecognized command \"{args[0]}\"");
                }
            }
            else
            {
                // Retrieve and save all the new infromation from Electricity & Gas
                // Electricity
                List<DataValuesModel> tempNameElectricityNew = await NewHistoryElectricity();

                if (tempNameElectricityNew.Count > 0)
                {
                    await _dataValues.SaveListDataValuesAsync(tempNameElectricityNew);
                    Console.WriteLine($"{tempNameElectricityNew.Count} New electricity records found and saved since last update");
                }
                else
                {
                    Console.WriteLine("No new electricity records found since last update");
                }

                // Gas
                List<DataValuesModel> tempNameGasNew = await NewHistoryGas();

                if (tempNameGasNew.Count > 0)
                {
                    await _dataValues.SaveListDataValuesAsync(tempNameGasNew);
                    Console.WriteLine($"{tempNameGasNew.Count} New gas records found and saved since last update");
                }
                else
                {
                    Console.WriteLine("No new gas records found since last update");
                }
            }
        }

        private List<DataValuesModel> MapApiToDatabase(ApiModel apiModel, DataSourcesModel dataSource)
        {
            List<DataValuesModel> output = new List<DataValuesModel>();
            foreach (var item in apiModel.Results)
            {
                output.Add(new DataValuesModel()
                {
                    Data_source_id = dataSource.Data_source_id,
                    Data_Value = item.Consumption,
                    Data_interval_start_datetime = item.Interval_start.DateTime,
                    Data_interval_start_offset = item.Interval_start.Offset,
                    Data_interval_end_datetime = item.Interval_end.DateTime,
                    Data_interval_end_offset = item.Interval_end.Offset
                });
            }

            return output;
        }

        private async Task<List<DataValuesModel>> NewHistoryElectricity()
        {
            // Retrieve config values
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            // Retrieve latest record from database and the data source id
            DataValuesModel lastRecordElectricity = await _dataValues.RetrieveLastRecordForSourceAsync("Electricity");
            DataSourcesModel electricityModel = await _dataSources.GetDataSourceIdFromName("Electricity");

            // Variables
            List<DataValuesModel> returnList = new List<DataValuesModel>();
            int page = 1;
            int useCount = 0;

            while (true)
            {
                // Get a page of values
                ApiModel temp = await _octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber);

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

                // Parse from ApiModel to List<DataValuesModel>
                List<DataValuesModel> tempList = MapApiToDatabase(temp, electricityModel);

                // Look at each record and determine if the last record in the database has been reached
                foreach (var item in tempList)
                {
                    // TODO: look at a way to incorporate a way to determine if two instances of a class hold the same values determining them as "equal" 
                    //  even if they are different instances of a class.
                    bool tempBoolTest = item.Data_source_id == lastRecordElectricity.Data_source_id &
                                        item.Data_Value == lastRecordElectricity.Data_Value &
                                        item.Data_interval_start_datetime == lastRecordElectricity.Data_interval_start_datetime &
                                        item.Data_interval_start_offset == lastRecordElectricity.Data_interval_start_offset &
                                        item.Data_interval_end_datetime == lastRecordElectricity.Data_interval_end_datetime &
                                        item.Data_interval_end_offset == lastRecordElectricity.Data_interval_end_offset;

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

        private async Task<List<DataValuesModel>> NewHistoryGas()
        {
            // Retrieve config values
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            // Retrieve latest record from database
            DataValuesModel lastRecordGas = await _dataValues.RetrieveLastRecordForSourceAsync("Gas");
            DataSourcesModel gasModel = await _dataSources.GetDataSourceIdFromName("Gas");

            // Variables
            List<DataValuesModel> returnList = new List<DataValuesModel>();
            int page = 1;
            int useCount = 0;

            while (true)
            {
                // Get a page of values
                ApiModel temp = await _octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber);

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
                List<DataValuesModel> tempList = MapApiToDatabase(temp, gasModel);

                // Look at each record and determine if the last record in the database has been reached
                foreach (var item in tempList)
                {
                    // TODO: look at a way to incorporate a way to determine if two instances of a class hold the same values determining them as "equal" 
                    //  even if they are different instances of a class.
                    bool tempBoolTest = item.Data_source_id == lastRecordGas.Data_source_id &
                                        item.Data_Value == lastRecordGas.Data_Value &
                                        item.Data_interval_start_datetime == lastRecordGas.Data_interval_start_datetime &
                                        item.Data_interval_start_offset == lastRecordGas.Data_interval_start_offset &
                                        item.Data_interval_end_datetime == lastRecordGas.Data_interval_end_datetime &
                                        item.Data_interval_end_offset == lastRecordGas.Data_interval_end_offset;

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

        private async Task<List<List<DataValuesModel>>> AllHistoryElectricity()
        {
            // Retrieve config values
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

            // Call api to retrieve count or records to retrieve
            ApiModel tempUse = await _octopusElectricityHelper.GetConsumption(electricityMPAN, electricitySerialNumber);
            DataSourcesModel electricityModel = await _dataSources.GetDataSourceIdFromName("Electricity");

            double electricityPages = Math.Ceiling(tempUse.Count / 100d);

            List<List<DataValuesModel>> electricityHistory = new List<List<DataValuesModel>>();
            List<Task<ApiModel>> tasks = new List<Task<ApiModel>>();

            for (int page = 1; page < (electricityPages + 1); page++)
            {
                tasks.Add(_octopusElectricityHelper.GetConsumptionPage(page, electricityMPAN, electricitySerialNumber));
            }

            var results = await Task.WhenAll(tasks);
            int countOfRetrievedRecords = 0;
            foreach (var item in results)
            {
                List<DataValuesModel> tempList = MapApiToDatabase(item, electricityModel);
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

        private async Task<List<List<DataValuesModel>>> AllHistoryGas()
        {
            // Retrieve config values
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

            // Call api to retrieve count or records to retrieve
            ApiModel tempUse = await _octopusGasHelper.GetConsumption(gasMPAN, gasSerialNumber);
            DataSourcesModel gasModel = await _dataSources.GetDataSourceIdFromName("Gas");

            double gasPages = Math.Ceiling(tempUse.Count / 100d);

            List<List<DataValuesModel>> gasHistory = new List<List<DataValuesModel>>();
            List<Task<ApiModel>> task = new List<Task<ApiModel>>();

            for (int page = 1; page < (gasPages + 1); page++)
            {
                task.Add(_octopusGasHelper.GetConsumptionPage(page, gasMPAN, gasSerialNumber));
            }

            var results = await Task.WhenAll(task);
            int countOfRetrievedRecords = 0;
            foreach (var item in results)
            {
                List<DataValuesModel> tempList = MapApiToDatabase(item, gasModel);
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
