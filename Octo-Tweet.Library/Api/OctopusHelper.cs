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
        public async Task<ApiModel> GetConsumption(string energySource, string mpan, string serialNumber)
        {
            string urlPath = $"/v1/{ energySource.ToLower() }-meter-points/{ mpan }/meters/{ serialNumber }/consumption/";

            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync(urlPath))
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
        public async Task<ApiModel> GetConsumptionPage(string energySource, double page, string mpan, string serialNumber)
        {
            string urlPath = $"/v1/{ energySource.ToLower() }-meter-points/{ mpan }/meters/{ serialNumber }/consumption/?page={ page }";

            using (HttpResponseMessage response = await _apiHelper.ApiClient.GetAsync(urlPath))
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
