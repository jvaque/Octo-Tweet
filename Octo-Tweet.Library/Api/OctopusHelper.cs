using Octo_Tweet.Library.Models;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public class OctopusHelper : IOctopusHelper
    {
        private readonly IAPIHelper _apiHelper;

        public OctopusHelper(IAPIHelper apiHelper)
        {
            _apiHelper = apiHelper;
        }

        public async Task<ElectricityModel> GetElectricityConsumption(string electricityMPAN, string electricitySerialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/electricity-meter-points/{ electricityMPAN }/meters/{ electricitySerialNumber }/consumption/"))
            {
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadAsAsync<ElectricityModel>();
                    return result;
                }
                else
                {
                    throw new Exception(response.ReasonPhrase);
                }
            }
        }

        public async Task<GasModel> GetGasConsumption(string gasMPAN, string gasSerialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/gas-meter-points/{ gasMPAN }/meters/{ gasSerialNumber }/consumption/"))
            {
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadAsAsync<GasModel>();
                    return result;
                }
                else
                {
                    throw new Exception(response.ReasonPhrase);
                }
            }
        }
    }
}
