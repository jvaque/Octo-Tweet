CREATE TABLE IF NOT EXISTS `octo_tweet`.`Chart_Tracker` (
    `chart_tracker_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `data_source_id` int UNSIGNED NOT NULL,
    `chart_type` varchar(255) NOT NULL,
    `chart_last_from` datetime NOT NULL,
    `chart_last_to` datetime NOT NULL,
    `chart_next_from` datetime NOT NULL,
    `chart_next_to` datetime NOT NULL,

    PRIMARY KEY (`chart_tracker_id`),
    CONSTRAINT FK_dataSource_ChartTracker FOREIGN KEY (`data_source_id`) REFERENCES `Data_Sources`(`data_source_id`),
    INDEX (`chart_next_to`),
    UNIQUE KEY UC_chart_type (`data_source_id`, `chart_type`)
) AUTO_INCREMENT = 1000;
