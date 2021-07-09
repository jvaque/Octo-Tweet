DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataValues_SelectDailyConsumptionFromRange`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataValues_SelectDailyConsumptionFromRange`(
    IN Source_name varchar(255),
    IN Interval_datetime_from datetime,
    IN Interval_datetime_to datetime
)
BEGIN

    SELECT
        MIN(`data_value_id`),
        MIN(`Data_Values`.`data_source_id`),
        SUM(`data_value`),
        MIN(DATE(`data_interval_start_datetime`)) AS data_interval_start_date,
        MIN(`data_interval_start_offset`),
        MAX(DATE(`data_interval_end_datetime`)) AS data_interval_end_date,
        MAX(`data_interval_end_offset`)
    FROM
        `Data_Values`
    LEFT JOIN `Data_Sources` ON
        (`Data_Values`.`data_source_id` = `Data_Sources`.`data_source_id`)
    WHERE
        (`Data_Sources`.`data_source_name` = Source_name)
        AND
        (`data_interval_start_datetime` >= Interval_datetime_from)
        AND
        (`data_interval_end_datetime` <= Interval_datetime_to)
    GROUP BY
        DATE(`data_interval_start_datetime`)
    ORDER BY
        DATE(`data_interval_start_datetime`) ASC
    ;

END

//

DELIMITER ;
