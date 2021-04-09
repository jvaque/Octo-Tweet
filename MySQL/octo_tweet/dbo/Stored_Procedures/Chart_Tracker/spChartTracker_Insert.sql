DROP PROCEDURE IF EXISTS `octo_tweet`.`spChartTracker_Insert`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spChartTracker_Insert`(
    IN Data_source_id int,
    IN Chart_type varchar(255),
    IN Chart_last_from datetime,
    IN Chart_last_to datetime,
    IN Chart_next_from datetime,
    IN Chart_next_to datetime
)
BEGIN

    INSERT INTO `Chart_Tracker`(
        `data_source_id`,
        `chart_type`,
        `chart_last_from`,
        `chart_last_to`,
        `chart_next_from`,
        `chart_next_to`)
    VALUES
        (
            Data_source_id,
            Chart_type,
            Chart_last_from,
            Chart_last_to,
            Chart_next_from,
            Chart_next_to
        )
    ;

END

//

DELIMITER ;
