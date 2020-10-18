CREATE TABLE IF NOT EXISTS octo_tweet.Electricity (
    electricity_id int UNSIGNED NOT NULL AUTO_INCREMENT,
    electricity_consumption float NOT NULL,
    electricity_interval_start_datetime datetime NOT NULL,
    electricity_interval_start_offset time NOT NULL,
    electricity_interval_end_datetime datetime NOT NULL,
    electricity_interval_end_offset time NOT NULL,

    PRIMARY KEY (electricity_id),
    INDEX (electricity_interval_start_datetime),
    INDEX (electricity_interval_end_datetime),
    UNIQUE KEY UC_electricity_interval_start_datetime (electricity_interval_start_datetime),
    UNIQUE KEY UC_electricity_interval_end_datetime (electricity_interval_end_datetime)
) AUTO_INCREMENT = 1000;

-- Engine and charset????