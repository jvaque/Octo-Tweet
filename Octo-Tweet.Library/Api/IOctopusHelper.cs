using Octo_Tweet.Library.Models;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public interface IOctopusHelper
    {
        Task<ApiModel> GetConsumption(string energySource, string mpan, string serialNumber);
        Task<ApiModel> GetConsumptionPage(string energySource, double page, string mpan, string serialNumber);
    }
}