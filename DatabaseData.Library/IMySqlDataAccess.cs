using System.Collections.Generic;
using System.Threading.Tasks;

namespace DatabaseData.Library
{
    public interface IMySqlDataAccess
    {
        string GetConnectionString(string name);
        Task<List<T>> LoadDataAsync<T, U>(string storedProcedure, U parameters, string conncetionStringName);
        Task SaveDataAsync<T>(string storedProcedure, T parameters, string connectionStringName);
    }
}