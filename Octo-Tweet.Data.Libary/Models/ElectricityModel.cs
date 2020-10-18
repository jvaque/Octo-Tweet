using System;
using System.Collections.Generic;
using System.Text;

namespace Octo_Tweet.Data.Libary.Models
{
    public class ElectricityModel
    {
        public int Electricity_id { get; set; }
        public float Electricity_consumption { get; set; }
        public DateTime Electricity_interval_start_datetime { get; set; }
        public TimeSpan Electricity_interval_start_offset { get; set; }
        public DateTime Electricity_interval_end_datetime { get; set; }
        public TimeSpan Electricity_interval_end_offset { get; set; }
    }
}