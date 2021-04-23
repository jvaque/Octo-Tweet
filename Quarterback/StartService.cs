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
        private readonly IOctopusHelper _octopusHelper;
        private readonly IChartTracker _chartTracker;
        private readonly IDataSources _dataSources;
        private readonly IDataValues _dataValues;

        public StartService(
            IConfiguration config, 
            IOctopusHelper octopusHelper,
            IChartTracker chartTracker,
            IDataSources dataSources,
            IDataValues dataValues
            )
        {
            _config = config;
            _octopusHelper = octopusHelper;
            _chartTracker = chartTracker;
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
                    List<Task<List<List<DataValuesModel>>>> tasksHistory = new List<Task<List<List<DataValuesModel>>>>
                    {
                        // Electricity
                        AllHistory("Electricity"),
                        // Gas
                        AllHistory("Gas")
                    };
                    List<List<DataValuesModel>>[] results = await Task.WhenAll(tasksHistory);

                    // Save all results to database
                    List<Task> tasks = new List<Task>();
                    foreach (var item in results)
                    {
                        foreach (var listDataValues in item)
                        {
                            tasks.Add(_dataValues.SaveListDataValuesAsync(listDataValues));
                        }
                    }
                    await Task.WhenAll(tasks);
                }
                else if (args[0] == "-c" || args[0] == "--chart-tracker-fill")
                {
                    await InitialChartTrackerFill("Electricity");
                    await InitialChartTrackerFill("Gas");
                }
                else
                {
                    Console.WriteLine($"Unrecognized command \"{args[0]}\"");
                }
            }
            else
            {
                // Retrieve and save all the new infromation from Electricity & Gas
                string[] tables = { "Electricity", "Gas" };
                List<Task<List<DataValuesModel>>> tasksNewHistory = new List<Task<List<DataValuesModel>>>();
                foreach (var table in tables)
                {
                    tasksNewHistory.Add(NewHistory(table));
                }
                List<DataValuesModel>[] results = await Task.WhenAll(tasksNewHistory);

                // Save results to database
                List<Task> tasks = new List<Task>();
                foreach (var item in results)
                {
                    if (item.Count > 0)
                    {
                        tasks.Add(_dataValues.SaveListDataValuesAsync(item));
                    }
                }
                await Task.WhenAll(tasks);

                // Display messages once everything is saved
                for (int i = 0; i < results.Length; i++)
                {
                    if (results[i].Count > 0)
                    {
                        Console.WriteLine($"{results[i].Count} New {tables[i]} records found and saved since last update");
                    }
                    else
                    {
                        Console.WriteLine($"No new {tables[i]} records found since last update");
                    }
                }
            }
        }

        private async Task InitialChartTrackerFill(string chartsTarget)
        {
            // Get first record
            DataValuesModel firstRecordEnergySource = await _dataValues.RetrieveFirstRecordForSourceAsync(chartsTarget);
            DataSourcesModel energySourceModel = await _dataSources.GetDataSourceIdFromName(chartsTarget);

            List<ChartTrackerModel> chartsToMake = new List<ChartTrackerModel>();

            // Add daily chart
            chartsToMake.Add(new ChartTrackerModel
            {
                Data_source_id = energySourceModel.Data_source_id,
                Chart_type = "Daily",
                Chart_last_from = firstRecordEnergySource.Data_interval_start_datetime.Date - TimeSpan.FromDays(1),
                Chart_last_to = firstRecordEnergySource.Data_interval_start_datetime.Date,
                Chart_next_from = firstRecordEnergySource.Data_interval_start_datetime.Date,
                Chart_next_to = firstRecordEnergySource.Data_interval_start_datetime.Date + TimeSpan.FromDays(1)
            });

            // Add weekly chart
            DateTime firstMonday = firstRecordEnergySource.Data_interval_start_datetime.Date;
            while (firstMonday.DayOfWeek != DayOfWeek.Monday)
            {
                firstMonday -= TimeSpan.FromDays(1);
            }
            chartsToMake.Add(new ChartTrackerModel
            {
                Data_source_id = energySourceModel.Data_source_id,
                Chart_type = "Weekly",
                Chart_last_from = firstMonday - TimeSpan.FromDays(7),
                Chart_last_to = firstMonday,
                Chart_next_from = firstMonday,
                Chart_next_to = firstMonday + TimeSpan.FromDays(7)
            });

            // Add monthly chart
            DateTime firstMonth = firstRecordEnergySource.Data_interval_start_datetime.Date;
            firstMonth -= TimeSpan.FromDays(firstMonth.Day - 1);
            chartsToMake.Add(new ChartTrackerModel
            {
                Data_source_id = energySourceModel.Data_source_id,
                Chart_type = "Monthly",
                Chart_last_from = firstMonth.AddMonths(-1),
                Chart_last_to = firstMonth,
                Chart_next_from = firstMonth,
                Chart_next_to = firstMonth.AddMonths(1)
            });
            // Add quaterly chart

            DateTime quarterStart = firstMonth;
            while (quarterStart.Month != 1 && quarterStart.Month != 3 && quarterStart.Month != 6 && quarterStart.Month != 9)
            {
                quarterStart = quarterStart.AddMonths(-1);
            }
            chartsToMake.Add(new ChartTrackerModel
            {
                Data_source_id = energySourceModel.Data_source_id,
                Chart_type = "Quarterly",
                Chart_last_from = quarterStart.AddMonths(-3) - TimeSpan.FromDays(7),
                Chart_last_to = quarterStart + TimeSpan.FromDays(7),
                Chart_next_from = quarterStart - TimeSpan.FromDays(7),
                Chart_next_to = quarterStart.AddMonths(3) + TimeSpan.FromDays(7)
            });
            // Add yearly chart

            DateTime yearStart = quarterStart.AddMonths(1 - quarterStart.Month);
            chartsToMake.Add(new ChartTrackerModel
            {
                Data_source_id = energySourceModel.Data_source_id,
                Chart_type = "Yearly",
                Chart_last_from = yearStart.AddMonths(-12) - TimeSpan.FromDays(14),
                Chart_last_to = yearStart + TimeSpan.FromDays(14),
                Chart_next_from = yearStart - TimeSpan.FromDays(14),
                Chart_next_to = yearStart.AddMonths(12) + TimeSpan.FromDays(14)
            });
            // Add rolling yearly chart
            // Save charts to make
            await _chartTracker.SaveChartsToTrackerAsync(chartsToMake);
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

        private async Task<List<DataValuesModel>> NewHistory(string energySource)
        {
            // Retrieve config values
            string energySourceMPAN = _config.GetValue<string>($"OctopusApi:{energySource}:mpan");
            string energySourceSerialNumber = _config.GetValue<string>($"OctopusApi:{energySource}:serial_number");

            // Retrieve latest record from database and the data source id
            DataValuesModel lastRecordEnergySource = await _dataValues.RetrieveLastRecordForSourceAsync(energySource);
            DataSourcesModel energySourceModel = await _dataSources.GetDataSourceIdFromName(energySource);

            // Variables
            List<DataValuesModel> returnList = new List<DataValuesModel>();
            int page = 1;
            int useCount = 0;

            while (true)
            {
                // Get a page of values
                ApiModel temp = await _octopusHelper.GetConsumptionPage(energySource, page, energySourceMPAN, energySourceSerialNumber);

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
                List<DataValuesModel> tempList = MapApiToDatabase(temp, energySourceModel);

                // Look at each record and determine if the last record in the database has been reached
                foreach (var item in tempList)
                {
                    // TODO: look at a way to incorporate a way to determine if two instances of a class hold the same values determining them as "equal" 
                    //  even if they are different instances of a class.
                    bool tempBoolTest = item.Data_source_id == lastRecordEnergySource.Data_source_id &
                                        item.Data_Value == lastRecordEnergySource.Data_Value &
                                        item.Data_interval_start_datetime == lastRecordEnergySource.Data_interval_start_datetime &
                                        item.Data_interval_start_offset == lastRecordEnergySource.Data_interval_start_offset &
                                        item.Data_interval_end_datetime == lastRecordEnergySource.Data_interval_end_datetime &
                                        item.Data_interval_end_offset == lastRecordEnergySource.Data_interval_end_offset;

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

        private async Task<List<List<DataValuesModel>>> AllHistory(string energySource)
        {
            // Retrieve config values
            string energySourceMPAN = _config.GetValue<string>($"OctopusApi:{energySource}:mpan");
            string energySourceSerialNumber = _config.GetValue<string>($"OctopusApi:{energySource}:serial_number");

            // Call api to retrieve count or records to retrieve
            ApiModel tempUse = await _octopusHelper.GetConsumption(energySource, energySourceMPAN, energySourceSerialNumber);
            DataSourcesModel energySourceModel = await _dataSources.GetDataSourceIdFromName(energySource);

            double energySourcePages = Math.Ceiling(tempUse.Count / 100d);

            List<List<DataValuesModel>> energySourceHistory = new List<List<DataValuesModel>>();
            List<Task<ApiModel>> tasks = new List<Task<ApiModel>>();

            for (int page = 1; page < (energySourcePages + 1); page++)
            {
                tasks.Add(_octopusHelper.GetConsumptionPage(energySource, page, energySourceMPAN, energySourceSerialNumber));
            }

            var results = await Task.WhenAll(tasks);
            int countOfRetrievedRecords = 0;
            foreach (var item in results)
            {
                List<DataValuesModel> tempList = MapApiToDatabase(item, energySourceModel);
                countOfRetrievedRecords += tempList.Count;
                energySourceHistory.Add(tempList);
            }

            if (tempUse.Count == countOfRetrievedRecords)
            {
                return energySourceHistory;
            }
            else
            {
                // TODO: Find a more elegant way to handle the error
                throw new Exception();
            }
        }
    }
}
