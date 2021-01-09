using DatabaseData.Library;
using Octo_Tweet.Data.Libary.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public class Electricity : IElectricity
    {
        private readonly IMySqlDataAccess _mySql;

        public Electricity(IMySqlDataAccess _mySql)
        {
            this._mySql = _mySql;
        }

        public async Task SaveListElectricityAsync(List<ElectricityModel> electricityList)
        {
            await _mySql.SaveDataAsync("spElectricity_Insert", electricityList, "octopus_database");
        }

        public async Task<ElectricityModel> RetrieveLastRecordElectricityAsync()
        {
            return (await _mySql.LoadDataAsync<ElectricityModel, dynamic>("spElectricity_GetLatestSavedRecord", new { }, "octopus_database")).FirstOrDefault();
        }
    }
}