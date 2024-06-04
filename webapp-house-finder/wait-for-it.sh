#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
port="$2"
timeout=30 # Increase timeout to 30 seconds (or adjust as needed)

echo "Waiting for $host:$port to become available..."

# Attempt to connect to the host and port until successful or timeout
until nc -z "$host" "$port"; do
  sleep 1
  timeout=$((timeout - 1))
  if [ $timeout -eq 0 ]; then
    echo "Timeout reached. Unable to connect to $host:$port."
    exit 1
  fi
done

echo "$host:$port is available!"