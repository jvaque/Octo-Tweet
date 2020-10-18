using System;
using System.Collections.Generic;
using System.Text;

namespace Octo_Tweet.Data.Libary.Models
{
    public class GasModel
    {
        public int Gas_id { get; set; }
        public float Gas_consumption { get; set; }
        public DateTime Gas_interval_start_datetime { get; set; }
        public TimeSpan Gas_interval_start_offset { get; set; }
        public DateTime Gas_interval_end_datetime { get; set; }
        public TimeSpan Gas_interval_end_offset { get; set; }
    }
}
