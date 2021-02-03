CREATE OR REPLACE VIEW `octo_tweet`.`routines_view`
AS
    SELECT
        `routine_name`,
        `routine_schema`
    FROM
        `information_schema`.`routines`
    WHERE 
        (`routine_type` = 'PROCEDURE')
        AND
        (`routine_schema` = 'octo_tweet')
    ;