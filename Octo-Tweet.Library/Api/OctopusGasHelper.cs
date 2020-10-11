using Octo_Tweet.Library.Models;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public class OctopusGasHelper : IOctopusGasHelper
    {
        private readonly IAPIHelper _apiHelper;

        public OctopusGasHelper(IAPIHelper apiHelper)
        {
            _apiHelper = apiHelper;
        }

        public async Task<GasModel> GetConsumption(string mpan, string serialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/gas-meter-points/{ mpan }/meters/{ serialNumber }/consumption/"))
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
