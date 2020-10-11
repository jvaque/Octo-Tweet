using Octo_Tweet.Library.Models;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public interface IOctopusElectricityHelper
    {
        Task<ElectricityModel> GetConsumption(string mpan, string serialNumber);
    }
}