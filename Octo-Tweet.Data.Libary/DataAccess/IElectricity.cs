using Octo_Tweet.Data.Libary.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Octo_Tweet.Data.Libary.DataAccess
{
    public interface IElectricity
    {
        Task SaveListElectricityAsync(List<ElectricityModel> electricityList);
    }
}