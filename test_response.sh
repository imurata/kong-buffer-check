#!/bin/bash

# URL and payload file
URL="http://localhost:8000/server/response-buffer"
REPEAT_COUNT=10  # Number of repetitions

# Initialize variables
TOTAL_CONNECT=0
TOTAL_TTFB=0
TOTAL_TOTAL_TIME=0

if [ -n "$1" ]; then
  echo $1
fi

# Execute curl and calculate averages
echo "Results:"
for i in $(seq 1 $REPEAT_COUNT); do
    echo "Run $i..."

    # Capture curl output
    OUTPUT=$(curl -XPOST -o /dev/null \
        -H 'Cache-Control: no-cache' \
        -s \
        -w "Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total}\n" \
        $URL)

    echo "$OUTPUT"

    # Extract individual times
    CONNECT_TIME=$(echo "$OUTPUT" | awk -F' ' '{print $2}')
    TTFB_TIME=$(echo "$OUTPUT" | awk -F' ' '{print $4}')
    TOTAL_TIME=$(echo "$OUTPUT" | awk -F' ' '{print $7}')

    # Accumulate times
    TOTAL_CONNECT=$(echo "$TOTAL_CONNECT + $CONNECT_TIME" | bc -l)
    TOTAL_TTFB=$(echo "$TOTAL_TTFB + $TTFB_TIME" | bc -l)
    TOTAL_TOTAL_TIME=$(echo "$TOTAL_TOTAL_TIME + $TOTAL_TIME" | bc -l)
done

# Calculate averages
AVERAGE_CONNECT=$(echo "$TOTAL_CONNECT / $REPEAT_COUNT" | bc -l)
AVERAGE_TTFB=$(echo "$TOTAL_TTFB / $REPEAT_COUNT" | bc -l)
AVERAGE_TOTAL_TIME=$(echo "$TOTAL_TOTAL_TIME / $REPEAT_COUNT" | bc -l)

# Print averages
echo "Averages:"
printf "Connect: %.6f TTFB: %.6f Total time: %.6f\n" $AVERAGE_CONNECT $AVERAGE_TTFB $AVERAGE_TOTAL_TIME
