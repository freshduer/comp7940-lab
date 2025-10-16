#!/bin/bash

FILE="hello.c"

for i in {1..3}; do
    OUT_FILE="hello_$i"
    gcc "$FILE" -o "$OUT_FILE"
    ./"$OUT_FILE" &
done

wait
echo "compile finished."

