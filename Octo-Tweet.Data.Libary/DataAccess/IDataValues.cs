using Octo_Tweet.Data.Libary.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public interface IDataValues
    {
        Task<DataValuesModel> RetrieveLastRecordForSourceAsync(string sourceName);
        Task SaveListDataValuesAsync(List<DataValuesModel> dataList);
    }
}