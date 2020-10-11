using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Octo_Tweet.Library.Api;
using System.Threading.Tasks;

namespace Quarterback
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var host = Host.CreateDefaultBuilder()
                .ConfigureServices((context, services) =>
                {
                    services.AddSingleton<IAPIHelper, APIHelper>();

                    services.AddTransient<IOctopusHelper, OctopusHelper>();

                    services.AddTransient<IStartService, StartService>();
                })
                .Build();

            var svc = ActivatorUtilities.CreateInstance<StartService>(host.Services);
            await svc.Run();
        }
    }
}
