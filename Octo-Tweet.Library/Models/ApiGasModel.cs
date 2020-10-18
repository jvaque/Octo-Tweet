using System;

namespace Octo_Tweet.Library.Models
{
    public class ApiGasModel
    {
        public int Count { get; set; }
        public ConsumptionDetail[] Results { get; set; }
    }
}
