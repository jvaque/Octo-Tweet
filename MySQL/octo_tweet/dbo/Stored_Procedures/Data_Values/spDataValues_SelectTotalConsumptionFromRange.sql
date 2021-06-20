DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataValues_SelectTotalConsumptionFromRange`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataValues_SelectTotalConsumptionFromRange`(
    IN Source_name varchar(255),
    IN Interval_datetime_from datetime,
    IN Interval_datetime_to datetime
)
BEGIN

    SELECT
        `data_value_id`,
        `Data_Values`.`data_source_id`,
        SUM(`data_value`),
        MIN(`data_interval_start_datetime`),
        `data_interval_start_offset`,
        MAX(`data_interval_end_datetime`),
        `data_interval_end_offset`
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
    ORDER BY
        `data_interval_start_datetime` ASC
    ;

END

//

DELIMITER ;
