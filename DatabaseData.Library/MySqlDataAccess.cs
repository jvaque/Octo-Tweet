using Dapper;
using Microsoft.Extensions.Configuration;
using MySqlConnector;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DatabaseData.Library
{
    public class MySqlDataAccess : IMySqlDataAccess
    {
        private readonly IConfiguration _config;

        public MySqlDataAccess(IConfiguration config)
        {
            _config = config;
        }

        public string GetConnectionString(string name)
        {
            return _config.GetConnectionString(name);
        }

        public async Task<List<T>> LoadDataAsync<T, U>(string storedProcedure, U parameters, string conncetionStringName)
        {
            string connectionString = GetConnectionString(conncetionStringName);

            using (IDbConnection connection = new MySqlConnection(connectionString))
            {
                List<T> rows = (await connection.QueryAsync<T>(storedProcedure, parameters,
                    commandType: CommandType.StoredProcedure)).ToList();

                return rows;
            }
        }

        public async Task SaveDataAsync<T>(string storedProcedure, T parameters, string connectionStringName)
        {
            string connectionString = GetConnectionString(connectionStringName);

            using (IDbConnection connection = new MySqlConnection(connectionString))
            {
                connection.Open();

                using (IDbTransaction transaction = connection.BeginTransaction())
                {
                    await connection.ExecuteAsync(storedProcedure, parameters,
                        commandType: CommandType.StoredProcedure, transaction: transaction);

                    transaction.Commit();
                }
            }
        }
    }
}
