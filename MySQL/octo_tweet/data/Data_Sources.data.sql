call spDataSources_Insert('Electricity');
call spDataSources_Insert('Gas');

-- Electricity  -> 1000
-- Gas          -> 1001

-- Get id for 'Electricity' and 'Gas'
call spChartTracker_Insert(
    -- Data_source_id,
    'Daily',
    '2021-01-01 00:00:00',
    '2021-01-02 00:00:00',
    '2021-01-02 00:00:00',
    '2021-01-03 00:00:00');

call spChartTracker_Insert(
    -- Data_source_id,
    'Weekly',
    '2021-12-28 00:00:00',
    '2021-01-04 00:00:00',
    '2021-01-04 00:00:00',
    '2021-01-10 00:00:00');

call spChartTracker_Insert(
    -- Data_source_id,
    'Monthly',
    '2021-01-01 00:00:00',
    '2021-02-01 00:00:00',
    '2021-02-01 00:00:00',
    '2021-03-01 00:00:00');

-- The following charts don't really need usefull information in 
-- the datetimes from and to as the program most likely will be 
-- able to handle the edge cases

-- Quaterly chart needs 7 more days at either end in order to 
-- produce a good looking moving average of 7 days of data
call spChartTracker_Insert(
    -- Data_source_id,
    'Quarterly',
    '2020-12-25 00:00:00',
    '2021-04-08 00:00:00',
    '2021-03-25 00:00:00',
    '2021-07-08 00:00:00');

-- Yearly chart needs 14 more days at either end in order to 
-- produce a good looking moving average of 14 days of data
call spChartTracker_Insert(
    -- Data_source_id,
    'Yearly',
    '2019-12-18 00:00:00',
    '2021-01-15 00:00:00',
    '2020-12-18 00:00:00',
    '2022-01-15 00:00:00');

-- Rolling_Yearly chart needs 14 days at either end in order to 
-- produce a good looking moving averate of 14 days this will
-- be somewhat equivalent to the yearly chart but produced on the 
-- 2nd and 16th day of the month
call spChartTracker_Insert(
    -- Data_source_id,
    'Rolling_Yearly',
    '2020-12-18 00:00:00',
    '2020-12-18 00:00:00',
    '2020-12-18 00:00:00',
    '2020-12-18 00:00:00');

