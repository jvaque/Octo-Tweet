CREATE TABLE IF NOT EXISTS `octo_tweet`.`Data_Sources` (
    `data_source_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `data_source_name` varchar(255) NOT NULL,

    PRIMARY KEY (`data_source_id`),
    UNIQUE KEY UC_dataSources_data_source_name (`data_source_name`)
) AUTO_INCREMENT = 1000;
