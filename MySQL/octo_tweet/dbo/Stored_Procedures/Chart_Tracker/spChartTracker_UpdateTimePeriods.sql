DROP PROCEDURE IF EXISTS `octo_tweet`.`spChartTracker_UpdateTimePeriods`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spChartTracker_UpdateTimePeriods`(
    IN Chart_tracker_id int,
    IN Chart_last_from datetime,
    IN Chart_last_to datetime,
    IN Chart_next_from datetime,
    IN Chart_next_to datetime
)
BEGIN

    UPDATE
        `Chart_Tracker`
    SET
        `Chart_Tracker`.`chart_last_from` = Chart_last_from,
        `Chart_Tracker`.`chart_last_to` = Chart_last_to,
        `Chart_Tracker`.`chart_next_from` = Chart_next_from,
        `Chart_Tracker`.`chart_next_to` = Chart_next_to
    WHERE
        (`Chart_Tracker`.`chart_tracker_id` = Chart_tracker_id)
    ;

END

//

DELIMITER ;
