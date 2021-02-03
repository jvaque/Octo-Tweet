DROP PROCEDURE IF EXISTS `octo_tweet`.`spGas_Insert`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spGas_Insert`(
    IN Gas_consumption float,
    IN Gas_interval_start_datetime datetime,
    IN Gas_interval_start_offset time,
    IN Gas_interval_end_datetime datetime,
    IN Gas_interval_end_offset time
)
BEGIN

    INSERT INTO `Gas`(
        `gas_consumption`,
        `gas_interval_start_datetime`,
        `gas_interval_start_offset`,
        `gas_interval_end_datetime`,
        `gas_interval_end_offset`)
    VALUES
        (
            Gas_consumption,
            Gas_interval_start_datetime,
            Gas_interval_start_offset,
            Gas_interval_end_datetime,
            Gas_interval_end_offset
        )
    ;

END

//

DELIMITER ;
