using System.Collections.Generic;
using System.Text;

namespace Octo_Tweet.Library.Models
{
    public class ElectricityModel
    {
        public int Count { get; set; }
        public ConsumptionDetail[] Results { get; set; }
    }
}
