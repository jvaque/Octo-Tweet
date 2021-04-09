DROP PROCEDURE IF EXISTS `octo_tweet`.`spDataSources_Insert`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spDataSources_Insert`(
    IN Data_source_name varchar(255)
)
BEGIN

    INSERT INTO `Data_Sources`(
        `data_source_name`)
    VALUES
        (
            Data_source_name
        )
    ;

END

//

DELIMITER ;
