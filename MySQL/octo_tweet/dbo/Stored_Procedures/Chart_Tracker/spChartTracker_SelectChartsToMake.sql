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

-- Consider this future improvement, remove the Electricity and Gas tables and 
--  create a new table called Data_Values with similar structure but with an 
--  extra column for the data_source_id, this way this stored procedure could
--  be changed to take only the chart type and return the charts that it can
--  make
