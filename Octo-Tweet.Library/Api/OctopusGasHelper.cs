using Octo_Tweet.Library.Models;
using System;
using System.Net.Http;
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

        public async Task<ApiGasModel> GetConsumption(string mpan, string serialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/gas-meter-points/{ mpan }/meters/{ serialNumber }/consumption/"))
            {
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadAsAsync<ApiGasModel>();
                    return result;
                }
                else
                {
                    throw new Exception(response.ReasonPhrase);
                }
            }
        }
        public async Task<ApiGasModel> GetConsumptionPage(double page, string mpan, string serialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/gas-meter-points/{ mpan }/meters/{ serialNumber }/consumption/?page={ page }"))
            {
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadAsAsync<ApiGasModel>();
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
