# Octo-Tweet

## Modifiers for Quaterback (c# program):

`-a` or `--all`
Get all the history useful when deploying the program for the first time as subsequent calls require the database to hold some data within it.

`-c` or `--chart-tracker-fill`
Fills the chart tracker with data so the python program is able to start generating charts from the very beguining

## Modifiers for Striker (python program):

Probably best to use `-h` for help

- `charts` subsection:

This is followed by three fariables `datetime_from`, `datetime_to` and `charts`. Datetimes must be given in ISO format, calling this function will force the creation of the charts for the specified time period.

- `generate` subsection:

`-t` or `--tweet`
Default false, can set to true to tweet the charts generated

`-l` or `--lazy`
Skips generating charts and tweeting (ideal for a new environment with no previous charts generated)

`-f` or `--folders`
Makes sure that the folders the program need to run are in place, if they are not found they will be created, this is intended as the first command run in a new environment as it would be wastefull to constantly check every time the program is run.

## Other notes:

The charts added are Daily, Weekly, Monthly, Quaterly and Yearly (planning on adding a Rolling_Yearly chart in the future), all of the charts take in data from their selective time periods but both the Quaterly and Yearly chart take in extra data from both ends in order to produce a better looking chart once the rolling average is applied.