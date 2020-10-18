using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using DatabaseData.Library;
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

                    // Octo-Tweet.Library
                    services.AddTransient<IOctopusElectricityHelper, OctopusElectricityHelper>();
                    services.AddTransient<IOctopusGasHelper, OctopusGasHelper>();

                    // DatabaseData.Libary
                    services.AddTransient<IMySqlDataAccess, MySqlDataAccess>();

                    // otherproject.library
                    //services.AddTransient<IUserData, UserData>();

                    services.AddTransient<IStartService, StartService>();
                })
                .Build();

            var svc = ActivatorUtilities.CreateInstance<StartService>(host.Services);
            await svc.Run();
        }
    }
}
