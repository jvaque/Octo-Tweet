DROP PROCEDURE IF EXISTS octo_tweet.spElectricity_Insert;

DELIMITER //

CREATE PROCEDURE octo_tweet.spElectricity_Insert(
    IN Electricity_consumption float,
    IN Electricity_interval_start_datetime datetime,
    IN Electricity_interval_start_offset time,
    IN Electricity_interval_end_datetime datetime,
    IN Electricity_interval_end_offset time
)
BEGIN

    INSERT INTO Electricity(electricity_consumption, electricity_interval_start_datetime, electricity_interval_start_offset, electricity_interval_end_datetime, electricity_interval_end_offset)
    VALUES(Electricity_consumption, Electricity_interval_start_datetime, Electricity_interval_start_offset, Electricity_interval_end_datetime, Electricity_interval_end_offset);

END

//

DELIMITER ;