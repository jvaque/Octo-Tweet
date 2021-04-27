#--------------------------------------------------------------------------------------------------
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spChartTracker_Insert` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spChartTracker_SelectChartsToMake` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spChartTracker_UpdateTimePeriods` TO 'octo_tweet_sp'@'localhost';
#--------------------------------------------------------------------------------------------------
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataSources_Insert` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataSources_SelectAll` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataSources_SelectByName` TO 'octo_tweet_sp'@'localhost';
#--------------------------------------------------------------------------------------------------
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataValues_Insert` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataValues_SelectDailyConsumptionFromRange` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataValues_SelectFirstSavedRecord` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataValues_SelectLatestSavedRecord` TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE `octo_tweet`.`spDataValues_SelectRecordsFromRange` TO 'octo_tweet_sp'@'localhost';

FLUSH PRIVILEGES;
