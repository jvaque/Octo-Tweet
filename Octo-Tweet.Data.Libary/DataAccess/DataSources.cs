using DatabaseData.Library;
using Octo_Tweet.Data.Libary.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public class DataSources : IDataSources
    {
        private readonly IMySqlDataAccess _mySql;

        public DataSources(IMySqlDataAccess _mySql)
        {
            this._mySql = _mySql;
        }

        public async Task<DataSourcesModel> GetDataSourceIdFromName(string sourceName)
        {
            return (await _mySql.LoadDataAsync<DataSourcesModel, dynamic>("spDataSources_SelectByName", new { Data_source_name = sourceName }, "octopus_database")).FirstOrDefault();
        }
    }
}
