DROP PROCEDURE IF EXISTS `octo_tweet`.`spChartTracker_SelectChartsToMake`;

DELIMITER //

CREATE PROCEDURE `octo_tweet`.`spChartTracker_SelectChartsToMake`(
    IN Data_source_name varchar(255),
    IN Data_source_last_record datetime
)
BEGIN

    SELECT
        `chart_tracker_id`,
        `Chart_Tracker`.`data_source_id`,
        `chart_type`,
        `chart_last_from`,
        `chart_last_to`,
        `chart_next_from`,
        `chart_next_to`
    FROM
        `Chart_Tracker`
    LEFT JOIN `Data_Sources` ON
        (`Chart_Tracker`.`data_source_id` = `Data_Sources`.`data_source_id`)
    WHERE
        (`Data_Sources`.`data_source_name` = Data_source_name)
        AND
        (`chart_next_to` <= Data_source_last_record)
    ORDER BY
        `chart_last_from` DESC
    ;

END

//

DELIMITER ;

-- This stored procedure is to be changed to only take the chart type it's to
--  make and it will return the charts it can make, a even more advanced 
--  version of this program would just return all the charts it can make, 
--  checking on it's own for the last inserted record for each data_type
