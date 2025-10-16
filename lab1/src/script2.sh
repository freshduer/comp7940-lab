#!/bin/bash

LOGFILE="monitor-cpu-memory.log"

while true; do
    echo "==== $(date) ====" >> "$LOGFILE"
    top -b -n 1 | head -n 5 >> "$LOGFILE"
    echo "" >> "$LOGFILE"
    sleep 5
done

