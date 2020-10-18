using DatabaseData.Library;
using Octo_Tweet.Data.Libary.Models;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public class Gas : IGas
    {
        private readonly IMySqlDataAccess _mySql;

        public Gas(IMySqlDataAccess _mySql)
        {
            this._mySql = _mySql;
        }

        public async Task SaveListGasAsync(List<GasModel> gasList)
        {
            await _mySql.SaveDataAsync("spGas_Insert", gasList, "octopus_database");
        }
    }
}
