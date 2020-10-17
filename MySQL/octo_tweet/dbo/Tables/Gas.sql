CREATE TABLE IF NOT EXISTS octo_tweet.Gas (
    gas_id int UNSIGNED NOT NULL AUTO_INCREMENT,
    gas_consumption float NOT NULL,
    gas_interval_start_datetime datetime NOT NULL,
    gas_interval_start_offset time NOT NULL,
    gas_interval_end_datetime datetime NOT NULL,
    gas_interval_end_offset time NOT NULL,
    
    PRIMARY KEY (gas_id),
    INDEX (gas_interval_start_datetime),
    INDEX (gas_interval_end_datetime)
) AUTO_INCREMENT = 1000;