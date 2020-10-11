using System.Net.Http;

namespace Octo_Tweet.Library.Api
{
    public interface IAPIHelper
    {
        HttpClient ApiClient { get; }
    }
}