using System;
using System.Collections.Generic;
using System.Text;

namespace Octo_Tweet.Data.Libary.Models
{
    public class ChartTrackerModel
    {
        public int Chart_tracker_id { get; set; }
        public int Data_source_id { get; set; }
        public string Chart_type { get; set; }
        public DateTime Chart_last_from { get; set; }
        public DateTime Chart_last_to { get; set; }
        public DateTime Chart_next_from { get; set; }
        public DateTime Chart_next_to { get; set; }
    }
}
