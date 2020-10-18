using Octo_Tweet.Library.Models;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public interface IOctopusElectricityHelper
    {
        Task<ApiElectricityModel> GetConsumption(string mpan, string serialNumber);
        Task<ApiElectricityModel> GetConsumptionPage(double page, string mpan, string serialNumber);
    }
}