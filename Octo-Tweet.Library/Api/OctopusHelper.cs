using Microsoft.Extensions.Configuration;
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
        private readonly IConfiguration _config;
        private readonly IAPIHelper _apiHelper;

        public OctopusHelper(IConfiguration config, IAPIHelper apiHelper)
        {
            _config = config;
            _apiHelper = apiHelper;
        }

        public async Task<ElectricityModel> GetElectricityConsumption()
        {
            string electricityMPAN = _config.GetValue<string>("OctopusApi:Electricity:mpan");
            string electricitySerialNumber = _config.GetValue<string>("OctopusApi:Electricity:serial_number");

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

        public async Task<GasModel> GetGasConsumption()
        {
            string gasMPAN = _config.GetValue<string>("OctopusApi:Gas:mpan");
            string gasSerialNumber = _config.GetValue<string>("OctopusApi:Gas:serial_number");

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
