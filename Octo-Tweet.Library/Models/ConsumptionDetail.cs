using System;

namespace Octo_Tweet.Library.Models
{
    public class ConsumptionDetail
    {
        public float Consumption { get; set; }
        public DateTimeOffset Interval_start { get; set; }
        public DateTimeOffset Interval_end { get; set; }
    }

}
