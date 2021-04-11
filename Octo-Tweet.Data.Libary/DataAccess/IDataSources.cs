using Octo_Tweet.Data.Libary.Models;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public interface IDataSources
    {
        Task<DataSourcesModel> GetDataSourceIdFromName(string sourceName);
    }
}