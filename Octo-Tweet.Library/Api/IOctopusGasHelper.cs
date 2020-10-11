using Octo_Tweet.Library.Models;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public interface IOctopusGasHelper
    {
        Task<GasModel> GetConsumption(string mpan, string serialNumber);
    }
}