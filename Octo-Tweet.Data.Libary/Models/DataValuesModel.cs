using System;
using System.Collections.Generic;
using System.Text;

namespace Octo_Tweet.Data.Libary.Models
{
    public class DataValuesModel
    {
        public int Data_value_id { get; set; }
        public int Data_source_id { get; set; }
        public float Data_Value { get; set; }
        public DateTime Data_interval_start_datetime { get; set; }
        public TimeSpan Data_interval_start_offset { get; set; }
        public DateTime Data_interval_end_datetime { get; set; }
        public TimeSpan Data_interval_end_offset { get; set; }
    }
}
