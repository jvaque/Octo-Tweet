DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataSources_SelectByName`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataSources_SelectByName`(
    IN Data_source_name varchar(255)
)
BEGIN

    SELECT
        `data_source_id`,
        `Data_Sources`.`data_source_name`
    FROM
        `Data_Sources`
    WHERE
        (`Data_Sources`.`data_source_name` = Data_source_name)
    ORDER BY
        `data_source_id` ASC
    ;

END

//

DELIMITER ;
