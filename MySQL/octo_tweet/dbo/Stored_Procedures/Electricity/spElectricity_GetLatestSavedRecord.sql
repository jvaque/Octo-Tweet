DROP PROCEDURE IF EXISTS octo_tweet.spElectricity_GetLatestSavedRecord;

DELIMITER //

CREATE PROCEDURE octo_tweet.spElectricity_GetLatestSavedRecord()
BEGIN

    SELECT
        electricity_consumption,
        electricity_interval_start_datetime,
        electricity_interval_start_offset,
        electricity_interval_end_datetime,
        electricity_interval_end_offset
    FROM
        Electricity
    ORDER BY
        electricity_interval_start_datetime DESC
    LIMIT
        1
    ;

END

//

DELIMITER ;