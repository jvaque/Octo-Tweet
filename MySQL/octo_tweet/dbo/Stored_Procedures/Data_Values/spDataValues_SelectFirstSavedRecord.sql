DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataValues_SelectFirstSavedRecord`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataValues_SelectFirstSavedRecord`(
    IN Source_name varchar(255)
)
BEGIN

    SELECT
        `data_value_id`,
        `Data_Values`.`data_source_id`,
        `data_value`,
        `data_interval_start_datetime`,
        `data_interval_start_offset`,
        `data_interval_end_datetime`,
        `data_interval_end_offset`
    FROM
        `Data_Values`
    LEFT JOIN `Data_Sources` ON
        (`Data_Values`.`data_source_id` = `Data_Sources`.`data_source_id`)
    WHERE
        (`Data_Sources`.`data_source_name` = Source_name)
    ORDER BY
        `data_interval_start_datetime` ASC
    LIMIT
        1
    ;

END

//

DELIMITER ;