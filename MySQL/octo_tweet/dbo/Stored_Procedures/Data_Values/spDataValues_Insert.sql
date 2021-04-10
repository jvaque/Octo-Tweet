DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataValues_Insert`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataValues_Insert`(
    IN Data_source_id int,
    IN Data_value float,
    IN Data_interval_start_datetime datetime,
    IN Data_interval_start_offset time,
    IN Data_interval_end_datetime datetime,
    IN Data_interval_end_offset time
)
BEGIN

    INSERT INTO `Data_Values`(
        `data_source_id`,
        `data_value`,
        `data_interval_start_datetime`,
        `data_interval_start_offset`,
        `data_interval_end_datetime`,
        `data_interval_end_offset`)
    VALUES
        (
            Data_source_id,
            Data_value,
            Data_interval_start_datetime,
            Data_interval_start_offset,
            Data_interval_end_datetime,
            Data_interval_end_offset
        )
    ;

END

//

DELIMITER ;
