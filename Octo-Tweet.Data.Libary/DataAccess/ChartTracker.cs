using DatabaseData.Library;
using Octo_Tweet.Data.Libary.Models;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public class ChartTracker : IChartTracker
    {
        private readonly IMySqlDataAccess _mySql;

        public ChartTracker(IMySqlDataAccess _mySql)
        {
            this._mySql = _mySql;
        }

        public async Task SaveChartsToTrackerAsync(List<ChartTrackerModel> chartList)
        {
            await _mySql.SaveDataAsync("spChartTracker_Insert", chartList, "octopus_database");
        }
    }
}
