using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using DatabaseData.Library;
using Octo_Tweet.Library.Api;
using System.Threading.Tasks;
using Octo_Tweet.Data.Libary.DataAccess;

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

                    // Octo-Tweet.Library
                    services.AddTransient<IOctopusElectricityHelper, OctopusElectricityHelper>();
                    services.AddTransient<IOctopusGasHelper, OctopusGasHelper>();

                    // DatabaseData.Libary
                    services.AddTransient<IMySqlDataAccess, MySqlDataAccess>();

                    // Octo-Tweet.Data.Library
                    services.AddTransient<IElectricity, Electricity>();
                    services.AddTransient<IGas, Gas>();

                    services.AddTransient<IStartService, StartService>();
                })
                .Build();

            var svc = ActivatorUtilities.CreateInstance<StartService>(host.Services);
            await svc.Run();
        }
    }
}
