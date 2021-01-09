using Octo_Tweet.Data.Libary.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public interface IGas
    {
        Task SaveListGasAsync(List<GasModel> gasList);
        Task<GasModel> RetrieveLastRecordGasAsync();
    }
}