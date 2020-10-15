using Octo_Tweet.Library.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public interface IOctopusElectricityHelper
    {
        Task<ElectricityModel> GetConsumption(string mpan, string serialNumber);
        Task<ElectricityModel> GetConsumptionPage(double page, string mpan, string serialNumber);
    }
}