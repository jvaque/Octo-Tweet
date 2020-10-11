using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;

namespace Octo_Tweet.Library.Api
{
    public class APIHelper : IAPIHelper
    {
        private readonly IConfiguration _config;
        private HttpClient _apiClient;
        public APIHelper(IConfiguration config)
        {
            _config = config;
            InitializeClient();
        }

        public HttpClient ApiClient
        {
            get
            {
                return _apiClient;
            }
        }

        private void InitializeClient()
        {
            string api = _config.GetValue<string>("OctopusApi:BaseURL");
            string authenticationString = $"{_config.GetValue<string>("OctopusApi:ApiKey")}:";
            var base64EncodedAuthenticationString = Convert.ToBase64String(ASCIIEncoding.UTF8.GetBytes(authenticationString));

            _apiClient = new HttpClient();
            _apiClient.BaseAddress = new Uri(api);
            _apiClient.DefaultRequestHeaders.Accept.Clear();
            _apiClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            _apiClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", base64EncodedAuthenticationString);
        }
    }
}
