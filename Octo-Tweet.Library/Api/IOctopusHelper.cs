using Octo_Tweet.Library.Models;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public interface IOctopusHelper
    {
        Task<ElectricityModel> GetElectricityConsumption(string electricityMPAN, string electricitySerialNumber);
        Task<GasModel> GetGasConsumption(string gasMPAN, string gasSerialNumber);
    }
}