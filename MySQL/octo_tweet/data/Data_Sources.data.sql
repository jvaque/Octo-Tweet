call spDataSources_Insert('Electricity');
call spDataSources_Insert('Gas');

-- -- Rolling_Yearly chart needs 14 days at either end in order to 
-- -- produce a good looking moving averate of 14 days this will
-- -- be somewhat equivalent to the yearly chart but produced on the 
-- -- 2nd and 16th day of the month
-- call spChartTracker_Insert(
--     -- Data_source_id,
--     'Rolling_Yearly',
--     '2020-12-18 00:00:00',
--     '2020-12-18 00:00:00',
--     '2020-12-18 00:00:00',
--     '2020-12-18 00:00:00');
