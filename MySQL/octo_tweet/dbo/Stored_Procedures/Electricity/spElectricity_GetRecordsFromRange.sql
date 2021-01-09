DROP PROCEDURE IF EXISTS octo_tweet.spElectricity_GetRecordsFromRange;

DELIMITER //

CREATE PROCEDURE octo_tweet.spElectricity_GetRecordsFromRange(
    IN Interval_datetime_from datetime,
    IN Interval_datetime_to datetime
)
BEGIN

    SELECT
        electricity_id,
        electricity_consumption,
        electricity_interval_start_datetime,
        electricity_interval_start_offset,
        electricity_interval_end_datetime,
        electricity_interval_end_offset
    FROM
        Electricity
    WHERE
        electricity_interval_start_datetime >= Interval_datetime_from
    AND
        electricity_interval_end_datetime <= Interval_datetime_to
    ORDER BY
        electricity_interval_start_datetime ASC
    ;

END

//

DELIMITER ;