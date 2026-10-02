#!/bin/bash
# Build and run one step of the flight controller:  ./run.sh [1|2|3]  (default 1)
cd "$(dirname "$0")" || exit 1
STEP=${1:-1}
if make -s "step$STEP"; then
    "./step$STEP"
else
    echo "Build failed."
    exit 1
fi
