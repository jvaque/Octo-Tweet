DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataSources_SelectAll`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataSources_SelectAll`()
BEGIN

    SELECT
        `data_source_id`,
        `data_source_name`
    FROM
        `Data_Sources`
    ORDER BY
        `data_source_id` ASC
    ;

END

//

DELIMITER ;
