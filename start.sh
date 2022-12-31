#!/bin/bash
set -ex  # exit on any errors and debug

if test -z "$SERVICE"; then
    echo "Missing SERVICE variable"
    exit 1
fi

# shellcheck disable=SC2039
if [[ $SERVICE = "meter" ]]
then
  echo "*** Service: METER**"
  python3 -m simulator.services.meter
elif [[ $SERVICE = "pv-simulator" ]]
then
  echo echo "*** Service: PV SIMULATOR**"
  python3 -m simulator.services.pv_simulator
else
  echo "** Service: WEB **"
  python3 -m simulator.services.web
fi