using Octo_Tweet.Library.Models;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace Octo_Tweet.Library.Api
{
    public class OctopusElectricityHelper : IOctopusElectricityHelper
    {
        private readonly IAPIHelper _apiHelper;

        public OctopusElectricityHelper(IAPIHelper apiHelper)
        {
            _apiHelper = apiHelper;
        }

        public async Task<ApiModel> GetConsumption(string mpan, string serialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/electricity-meter-points/{ mpan }/meters/{ serialNumber }/consumption/"))
            {
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadAsAsync<ApiModel>();
                    return result;
                }
                else
                {
                    throw new Exception(response.ReasonPhrase);
                }
            }
        }

        public async Task<ApiModel> GetConsumptionPage(double page, string mpan, string serialNumber)
        {
            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync($"/v1/electricity-meter-points/{ mpan }/meters/{ serialNumber }/consumption/?page={ page }"))
            {
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadAsAsync<ApiModel>();
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
