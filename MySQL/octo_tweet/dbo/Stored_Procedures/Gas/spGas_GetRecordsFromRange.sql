DROP PROCEDURE IF EXISTS `octo_tweet`.`spGas_GetRecordsFromRange`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spGas_GetRecordsFromRange`(
    IN Interval_datetime_from datetime,
    IN Interval_datetime_to datetime
)
BEGIN

    SELECT
        `gas_id`,
        `gas_consumption`,
        `gas_interval_start_datetime`,
        `gas_interval_start_offset`,
        `gas_interval_end_datetime`,
        `gas_interval_end_offset`
    FROM
        `Gas`
    WHERE
        (`gas_interval_start_datetime` >= Interval_datetime_from)
        AND
        (`gas_interval_end_datetime` <= Interval_datetime_to)
    ORDER BY
        `gas_interval_start_datetime` ASC
    ;

END

//

DELIMITER ;