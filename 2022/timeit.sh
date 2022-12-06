#!/usr/bin/env bash

set -euo pipefail

echo "" > times.txt

for day in $(find . -type d | grep day); do
    echo "Day $(echo ${day} | tr -dc '0-9')" >> times.txt
    (time python3 ${day}/solution.py) 2>> times.txt
    echo "" >> times.txt
done