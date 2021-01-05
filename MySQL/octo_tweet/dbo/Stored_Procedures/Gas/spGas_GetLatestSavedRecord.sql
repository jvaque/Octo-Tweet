DROP PROCEDURE IF EXISTS octo_tweet.spGas_GetLatestSavedRecord;

DELIMITER //

CREATE PROCEDURE octo_tweet.spGas_GetLatestSavedRecord()
BEGIN

    SELECT
        gas_consumption,
        gas_interval_start_datetime,
        gas_interval_start_offset,
        gas_interval_end_datetime,
        gas_interval_end_offset
    FROM
        Gas
    ORDER BY
        gas_interval_start_datetime DESC
    LIMIT
        1
    ;

END

//

DELIMITER ;