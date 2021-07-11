#!/bin/sh
echo $(realpath $0)
cd /home/ubuntu/Octo-Tweet

# First get the latest records from the octopus api
(cd publish/ && ./Quarterback)

# Generate and tweet charts
. .venv/bin/activate
python Python/Striker.py generate --tweet
deactivate