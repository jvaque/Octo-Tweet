CREATE TABLE IF NOT EXISTS `octo_tweet`.`Data_Values` (
    `data_value_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `data_source_id` int UNSIGNED NOT NULL,
    `data_value` float NOT NULL,
    `data_interval_start_datetime` datetime NOT NULL,
    `data_interval_start_offset` time NOT NULL,
    `data_interval_end_datetime` datetime NOT NULL,
    `data_interval_end_offset` time NOT NULL,

    PRIMARY KEY (`data_value_id`),
    CONSTRAINT FK_dataSource_DataValues FOREIGN KEY (`data_source_id`) REFERENCES `Data_Sources`(`data_source_id`),
    INDEX (`data_interval_start_datetime`),
    INDEX (`data_interval_end_datetime`),
    UNIQUE KEY UC_data_interval_start (`data_source_id`, `data_interval_start_datetime`, `data_interval_start_offset`),
    UNIQUE KEY UC_data_interval_end (`data_source_id`, `data_interval_end_datetime`, `data_interval_end_offset`)
) AUTO_INCREMENT = 1000;

-- Engine and charset????