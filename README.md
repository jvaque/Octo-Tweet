# Octo-Tweet

## Modifiers for Quaterback (c# program):

-a or --all
Get all the history useful when deploying the program for the first time as subsequent calls require the database to hold some data within it.

-c or --chart-tracker-fill
Fills the chart tracker with data so the python program is able to start generating charts from the very beguining

## Modifiers for Striker (python program):


## Other notes:

The charts added are Daily, Weekly, Monthly, Quaterly and Yearly (planning on adding a Rolling_Yearly chart in the future), all of the charts take in data from their selective time periods but both the Quaterly and Yearly chart take in extra data from both ends in order to produce a better looking chart once the rolling average is applied.