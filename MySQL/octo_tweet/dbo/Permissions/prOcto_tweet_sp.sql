#--------------------------------------------------------------------------------------------------
GRANT EXECUTE ON PROCEDURE octo_tweet.spElectricity_GetLatestSavedRecord TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE octo_tweet.spElectricity_GetRecordsFromRange TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE octo_tweet.spElectricity_Insert TO 'octo_tweet_sp'@'localhost';
#--------------------------------------------------------------------------------------------------
GRANT EXECUTE ON PROCEDURE octo_tweet.spGas_GetLatestSavedRecord TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE octo_tweet.spGas_GetRecordsFromRange TO 'octo_tweet_sp'@'localhost';
GRANT EXECUTE ON PROCEDURE octo_tweet.spGas_Insert TO 'octo_tweet_sp'@'localhost';
#--------------------------------------------------------------------------------------------------

FLUSH PRIVILEGES;