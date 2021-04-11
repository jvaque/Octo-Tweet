using DatabaseData.Library;
using Octo_Tweet.Data.Libary.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public class DataValues : IDataValues
    {
        private readonly IMySqlDataAccess _mySql;

        public DataValues(IMySqlDataAccess _mySql)
        {
            this._mySql = _mySql;
        }

        public async Task SaveListDataValuesAsync(List<DataValuesModel> dataList)
        {
            await _mySql.SaveDataAsync("spDataValues_Insert", dataList, "octopus_database");
        }

        public async Task<DataValuesModel> RetrieveLastRecordForSourceAsync(string sourceName)
        {
            return (await _mySql.LoadDataAsync<DataValuesModel, dynamic>("spDataValues_SelectLatestSavedRecord", new { Source_name = sourceName }, "octopus_database")).FirstOrDefault();
        }
    }
}
